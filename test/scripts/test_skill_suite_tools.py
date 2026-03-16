from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_suite_tools as tools  # noqa: E402


class SkillSuiteToolsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.workspace_root = Path(self.temp_dir.name).resolve()
        self.iteration_dir = self.workspace_root / "test" / "iteration-9"
        self.iteration_dir.mkdir(parents=True, exist_ok=True)
        self._write_protocol_files()
        self._write_shared_specs()
        self._write_split_evals("create-element")

    def _write_protocol_files(self) -> None:
        for rel_path in tools.PROTOCOL_TRACKED_FILES:
            path = self.workspace_root / rel_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"stub for {rel_path}\n", encoding="utf-8")

    def _write_shared_specs(self) -> None:
        shared_root = self.workspace_root / "projects" / "shared"
        shared_root.mkdir(parents=True, exist_ok=True)
        (shared_root / "spec-global.c4").write_text(
            "specification {\n    relationship uses { notation 'Uses' }\n    relationship calls { notation 'Calls' }\n}\n",
            encoding="utf-8",
        )
        (shared_root / "spec-context.c4").write_text(
            "specification {\n    element System_External { }\n}\n",
            encoding="utf-8",
        )
        (shared_root / "spec-containers.c4").write_text(
            "specification {\n    element Container_Api { }\n    element Container_Webapp { }\n}\n",
            encoding="utf-8",
        )
        (shared_root / "spec-components.c4").write_text(
            "specification {\n    element Component { }\n}\n",
            encoding="utf-8",
        )
        (shared_root / "spec-deployment.c4").write_text(
            "specification {\n    deploymentNode Node_App { }\n}\n",
            encoding="utf-8",
        )

    def _write_split_evals(self, skill_name: str) -> tuple[Path, Path]:
        evals_dir = self.workspace_root / ".github" / "skills" / skill_name / "evals"
        evals_dir.mkdir(parents=True, exist_ok=True)
        public_path = evals_dir / "evals-public.json"
        grading_path = evals_dir / "grading-spec.json"
        public_path.write_text(
            json.dumps(
                {
                    "skill_name": skill_name,
                    "artifact_type": "evals-public",
                    "schema_version": tools.EVAL_ARTIFACT_SCHEMA_VERSION,
                    "evals": [
                        {
                            "id": 0,
                            "prompt": "Add an API container.",
                            "files": [],
                        }
                    ],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        grading_path.write_text(
            json.dumps(
                {
                    "skill_name": skill_name,
                    "artifact_type": "grading-spec",
                    "schema_version": tools.EVAL_ARTIFACT_SCHEMA_VERSION,
                    "evals": [
                        {
                            "id": 0,
                            "expected_output": "Use Container_Api.",
                            "files": [],
                            "expectations": ["Uses Container_Api", "Provides a concrete declaration"],
                        }
                    ],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return public_path, grading_path

    def _write_json(self, path: Path, data: dict) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        return path

    def test_split_eval_artifacts_load_and_grading_prompt_is_rejected(self) -> None:
        bundle = tools.load_split_eval_artifacts(self.workspace_root, "create-element")
        self.assertEqual(bundle["public"]["artifact_type"], "evals-public")
        self.assertEqual(bundle["grading"]["artifact_type"], "grading-spec")
        self.assertNotIn("prompt", bundle["grading"]["evals"][0])

        grading_path = self.workspace_root / ".github" / "skills" / "create-element" / "evals" / "grading-spec.json"
        grading_payload = tools.read_json(grading_path)
        grading_payload["evals"][0]["prompt"] = "This should not be here"
        tools.write_json(grading_path, grading_payload)

        with self.assertRaises(ValueError):
            tools.load_split_eval_artifacts(self.workspace_root, "create-element")

    def test_materialize_comparisons_rejects_incomplete_schema(self) -> None:
        raw_path = self._write_json(
            self.workspace_root / "raw-blind.json",
            {
                "comparisons": [
                    {
                        "eval_id": 0,
                        "winner": "A",
                        "reasoning": "A is better.",
                        "rubric": {
                            "A": {"overall_score": 8.0},
                            "B": {"overall_score": 5.0},
                        },
                        "expectation_results": {
                            "A": {"passed": 2, "total": 2, "pass_rate": 1.0},
                            "B": {"passed": 1, "total": 2, "pass_rate": 0.5},
                        },
                    }
                ]
            },
        )

        with self.assertRaises(ValueError):
            tools.materialize_blind_comparisons(self.iteration_dir, "create-element", raw_path)

    def test_protocol_preflight_writes_lock_file(self) -> None:
        manifest = tools.build_protocol_manifest(self.workspace_root, "benchmark-test")
        manifest_path = self.workspace_root / "test" / "benchmark-protocol.json"
        tools.write_json(manifest_path, manifest)

        summary = tools.freeze_protocol_for_iteration(self.iteration_dir, self.workspace_root, manifest_path)
        lock_path = self.workspace_root / summary["output_path"]

        self.assertTrue(lock_path.exists())
        lock_payload = tools.read_json(lock_path)
        self.assertEqual(lock_payload["protocol_version"], "benchmark-test")
        self.assertEqual(len(lock_payload["skill_eval_artifacts"]), 1)

    def test_benchmark_agent_plan_defaults_to_parallel_within_phase(self) -> None:
        plan = tools.benchmark_agent_plan(self.iteration_dir, skill="create-element")

        self.assertEqual(plan["parallelism"]["default_policy"], "parallel-within-phase")
        self.assertEqual(plan["parallelism"]["cross_phase_parallelism"], "forbidden")

        phases = {entry["phase"]: entry for entry in plan["phases"]}
        self.assertEqual(phases["without_skill"]["dispatch_mode"], "parallel")
        self.assertEqual(phases["with_skill"]["dispatch_mode"], "parallel")
        self.assertEqual(phases["blind_compare"]["dispatch_mode"], "parallel")

        self.assertTrue(
            any("parallel within each phase" in note for note in plan.get("notes", []))
        )

    def test_materialize_run_and_summarize_support_repeated_runs(self) -> None:
        raw_1 = self._write_json(
            self.workspace_root / "run-1.json",
            {
                "skill_name": "create-element",
                "configuration": "with_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:00:00Z",
                "finished_at": "2026-03-13T10:00:05Z",
                "responses": [{"id": 0, "response": "First answer"}],
            },
        )
        raw_2 = self._write_json(
            self.workspace_root / "run-2.json",
            {
                "skill_name": "create-element",
                "configuration": "with_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:01:00Z",
                "finished_at": "2026-03-13T10:01:08Z",
                "responses": [{"id": 0, "response": "Second answer with more words"}],
            },
        )

        tools.materialize_run_artifacts(self.iteration_dir, "create-element", "with_skill", raw_1, run_number=1)
        tools.materialize_run_artifacts(self.iteration_dir, "create-element", "with_skill", raw_2, run_number=2)

        summary = tools.summarize_config(
            self.iteration_dir / "create-element",
            "with_skill",
            self.workspace_root / ".github" / "skills" / "create-element" / "evals" / "evals-public.json",
        )

        self.assertEqual(summary["run_count"], 2)
        self.assertEqual(len(summary["runs"]), 2)
        self.assertIn("elapsed_seconds_per_eval", summary["variance"])
        self.assertTrue((self.iteration_dir / "create-element" / "eval-0" / "with_skill" / "run-2" / "response.md").exists())

    def test_validate_executable_checks_flags_unknown_kind(self) -> None:
        response_path = self.iteration_dir / "create-element" / "eval-0" / "with_skill" / "response.md"
        response_path.parent.mkdir(parents=True, exist_ok=True)
        response_path.write_text(
            "```likec4\nnewApi = Container_Imaginary \"Broken API\" {\n}\n```\n",
            encoding="utf-8",
        )

        summary = tools.validate_executable_checks(self.iteration_dir, self.workspace_root)
        self.assertEqual(summary["summary_count"], 2)

        checks_path = self.iteration_dir / "create-element" / "with_skill-executable-checks.json"
        checks = tools.read_json(checks_path)
        self.assertEqual(checks["summary"]["valid_eval_rate"], 0.0)
        self.assertIn("Unknown LikeC4 kind 'Container_Imaginary'.", checks["evals"][0]["snippets"][0]["errors"])


if __name__ == "__main__":
    unittest.main()
