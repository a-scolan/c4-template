from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import skill_suite_tools as tools  # noqa: E402
from benchmark.hook_runtime import resolve_audit_log_path, resolve_trace_level  # noqa: E402


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

    def _write_two_eval_split_evals(self, skill_name: str) -> tuple[Path, Path]:
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
                        {"id": 0, "prompt": "Add an API container.", "files": []},
                        {"id": 1, "prompt": "Add a Webapp container.", "files": []},
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
                        {"id": 0, "expected_output": "Use Container_Api.", "files": [], "expectations": ["Uses Container_Api"]},
                        {"id": 1, "expected_output": "Use Container_Webapp.", "files": [], "expectations": ["Uses Container_Webapp"]},
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

    def test_split_eval_artifacts_accept_execution_checks(self) -> None:
        grading_path = self.workspace_root / ".github" / "skills" / "create-element" / "evals" / "grading-spec.json"
        grading_payload = tools.read_json(grading_path)
        grading_payload["evals"][0]["execution_checks"] = [
            {
                "name": "Validate snippet",
                "description": "Run a lightweight validator when possible.",
                "when": "Run this when the response includes a concrete snippet.",
                "instructions": [
                    "Extract the snippet.",
                    "Validate it in isolation.",
                ],
                "success_signals": ["No validator errors are reported."],
                "failure_signals": ["Validator errors are reported."],
            }
        ]
        tools.write_json(grading_path, grading_payload)

        bundle = tools.load_split_eval_artifacts(self.workspace_root, "create-element")

        self.assertEqual(bundle["grading"]["evals"][0]["execution_checks"][0]["name"], "Validate snippet")

    def test_split_eval_artifacts_reject_malformed_execution_checks(self) -> None:
        grading_path = self.workspace_root / ".github" / "skills" / "create-element" / "evals" / "grading-spec.json"
        grading_payload = tools.read_json(grading_path)
        grading_payload["evals"][0]["execution_checks"] = [
            {
                "name": "",
                "instructions": [],
            }
        ]
        tools.write_json(grading_path, grading_payload)

        with self.assertRaises(ValueError):
            tools.load_split_eval_artifacts(self.workspace_root, "create-element")

    def test_split_eval_artifacts_accept_default_execution_checks(self) -> None:
        grading_path = self.workspace_root / ".github" / "skills" / "create-element" / "evals" / "grading-spec.json"
        grading_payload = tools.read_json(grading_path)
        grading_payload["default_execution_checks"] = [
            {
                "name": "Default validator",
                "instructions": ["Extract output.", "Run lightweight validator."],
                "success_signals": ["Validation succeeds."],
                "failure_signals": ["Validation fails."],
            }
        ]
        tools.write_json(grading_path, grading_payload)

        bundle = tools.load_split_eval_artifacts(self.workspace_root, "create-element")

        self.assertEqual(bundle["grading"]["default_execution_checks"][0]["name"], "Default validator")

    def test_split_eval_artifacts_reject_malformed_default_execution_checks(self) -> None:
        grading_path = self.workspace_root / ".github" / "skills" / "create-element" / "evals" / "grading-spec.json"
        grading_payload = tools.read_json(grading_path)
        grading_payload["default_execution_checks"] = [
            {
                "name": "",
                "instructions": [],
            }
        ]
        tools.write_json(grading_path, grading_payload)

        with self.assertRaises(ValueError):
            tools.load_split_eval_artifacts(self.workspace_root, "create-element")

    def test_build_grader_bundle_includes_execution_checks(self) -> None:
        grading_path = self.workspace_root / ".github" / "skills" / "create-element" / "evals" / "grading-spec.json"
        grading_payload = tools.read_json(grading_path)
        grading_payload["evals"][0]["execution_checks"] = [
            {
                "name": "Validate snippet",
                "instructions": ["Extract the snippet.", "Validate it in isolation."],
            }
        ]
        tools.write_json(grading_path, grading_payload)

        response_path = self.iteration_dir / "create-element" / "eval-0" / "with_skill" / "response.md"
        response_path.parent.mkdir(parents=True, exist_ok=True)
        response_path.write_text("```likec4\napi = Container_Api 'API'\n```\n", encoding="utf-8")

        bundle = tools.build_grader_bundle(self.iteration_dir, self.workspace_root, "create-element", 0, "with_skill")

        self.assertEqual(bundle["execution_checks"][0]["name"], "Validate snippet")

    def test_build_grader_bundle_merges_default_and_eval_execution_checks(self) -> None:
        grading_path = self.workspace_root / ".github" / "skills" / "create-element" / "evals" / "grading-spec.json"
        grading_payload = tools.read_json(grading_path)
        grading_payload["default_execution_checks"] = [
            {
                "name": "Validate snippet",
                "instructions": ["Default step."],
                "success_signals": ["Default success signal."],
            },
            {
                "name": "Generic syntax check",
                "instructions": ["Run generic check."],
            },
        ]
        grading_payload["evals"][0]["execution_checks"] = [
            {
                "name": "Validate snippet",
                "instructions": ["Eval override step."],
                "failure_signals": ["Eval-specific failure signal."],
            }
        ]
        tools.write_json(grading_path, grading_payload)

        response_path = self.iteration_dir / "create-element" / "eval-0" / "with_skill" / "response.md"
        response_path.parent.mkdir(parents=True, exist_ok=True)
        response_path.write_text("```likec4\napi = Container_Api 'API'\n```\n", encoding="utf-8")

        bundle = tools.build_grader_bundle(self.iteration_dir, self.workspace_root, "create-element", 0, "with_skill")

        self.assertEqual(len(bundle["default_execution_checks"]), 2)
        self.assertEqual(len(bundle["eval_execution_checks"]), 1)
        self.assertEqual(len(bundle["execution_checks"]), 2)
        self.assertEqual(bundle["execution_checks"][0]["name"], "Validate snippet")
        self.assertEqual(bundle["execution_checks"][0]["instructions"], ["Eval override step."])
        self.assertEqual(bundle["execution_checks"][1]["name"], "Generic syntax check")

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

    def test_materialize_comparisons_accepts_legacy_two_decimal_pass_rate_rounding(self) -> None:
        raw_path = self._write_json(
            self.workspace_root / "raw-blind-rounded.json",
            {
                "comparisons": [
                    {
                        "eval_id": 0,
                        "winner": "A",
                        "reasoning": "A is slightly better.",
                        "rubric": {
                            "A": {"content_score": 8.0, "structure_score": 8.0, "overall_score": 8.0},
                            "B": {"content_score": 7.0, "structure_score": 7.0, "overall_score": 7.0},
                        },
                        "expectation_results": {
                            "A": {"passed": 2, "total": 3, "pass_rate": 0.67},
                            "B": {"passed": 1, "total": 3, "pass_rate": 0.33},
                        },
                    }
                ]
            },
        )

        summary = tools.materialize_blind_comparisons(self.iteration_dir, "create-element", raw_path)

        self.assertEqual(summary["comparison_count"], 1)

    def test_materialize_comparisons_merges_without_overwriting_existing_entries(self) -> None:
        first_payload = self._write_json(
            self.workspace_root / "raw-blind-first.json",
            {
                "skill_name": "create-element",
                "comparisons": [
                    {
                        "eval_id": 0,
                        "run_number": 1,
                        "winner": "A",
                        "reasoning": "A is better on eval 0.",
                        "rubric": {
                            "A": {"content_score": 8.0, "structure_score": 8.0, "overall_score": 8.0},
                            "B": {"content_score": 6.0, "structure_score": 6.0, "overall_score": 6.0},
                        },
                        "expectation_results": {
                            "A": {"passed": 2, "total": 2, "pass_rate": 1.0},
                            "B": {"passed": 1, "total": 2, "pass_rate": 0.5},
                        },
                    }
                ],
            },
        )
        second_payload = self._write_json(
            self.workspace_root / "raw-blind-second.json",
            {
                "skill_name": "create-element",
                "comparisons": [
                    {
                        "eval_id": 1,
                        "run_number": 1,
                        "winner": "B",
                        "reasoning": "B is better on eval 1.",
                        "rubric": {
                            "A": {"content_score": 6.0, "structure_score": 6.0, "overall_score": 6.0},
                            "B": {"content_score": 8.0, "structure_score": 8.0, "overall_score": 8.0},
                        },
                        "expectation_results": {
                            "A": {"passed": 1, "total": 2, "pass_rate": 0.5},
                            "B": {"passed": 2, "total": 2, "pass_rate": 1.0},
                        },
                    }
                ],
            },
        )

        first = tools.materialize_blind_comparisons(self.iteration_dir, "create-element", first_payload)
        second = tools.materialize_blind_comparisons(self.iteration_dir, "create-element", second_payload)

        self.assertEqual(first["raw_comparison_count"], 1)
        self.assertEqual(first["comparison_count"], 1)
        self.assertEqual(first["added_count"], 1)
        self.assertEqual(first["replaced_count"], 0)

        self.assertEqual(second["raw_comparison_count"], 1)
        self.assertEqual(second["comparison_count"], 2)
        self.assertEqual(second["added_count"], 1)
        self.assertEqual(second["replaced_count"], 0)

        persisted = tools.read_json(self.iteration_dir / "create-element" / "blind-comparisons.json")
        self.assertEqual(len(persisted["comparisons"]), 2)
        self.assertEqual([item["eval_id"] for item in persisted["comparisons"]], [0, 1])

    def test_materialize_comparisons_replaces_existing_entry_same_eval_and_run(self) -> None:
        first_payload = self._write_json(
            self.workspace_root / "raw-blind-replace-1.json",
            {
                "skill_name": "create-element",
                "comparisons": [
                    {
                        "eval_id": 0,
                        "run_number": 2,
                        "winner": "A",
                        "reasoning": "Initial judgment.",
                        "rubric": {
                            "A": {"content_score": 8.0, "structure_score": 8.0, "overall_score": 8.0},
                            "B": {"content_score": 7.0, "structure_score": 7.0, "overall_score": 7.0},
                        },
                        "expectation_results": {
                            "A": {"passed": 2, "total": 2, "pass_rate": 1.0},
                            "B": {"passed": 1, "total": 2, "pass_rate": 0.5},
                        },
                    }
                ],
            },
        )
        second_payload = self._write_json(
            self.workspace_root / "raw-blind-replace-2.json",
            {
                "skill_name": "create-element",
                "comparisons": [
                    {
                        "eval_id": 0,
                        "run_number": 2,
                        "winner": "B",
                        "reasoning": "Re-evaluated judgment.",
                        "rubric": {
                            "A": {"content_score": 6.0, "structure_score": 6.0, "overall_score": 6.0},
                            "B": {"content_score": 9.0, "structure_score": 9.0, "overall_score": 9.0},
                        },
                        "expectation_results": {
                            "A": {"passed": 1, "total": 2, "pass_rate": 0.5},
                            "B": {"passed": 2, "total": 2, "pass_rate": 1.0},
                        },
                    }
                ],
            },
        )

        tools.materialize_blind_comparisons(self.iteration_dir, "create-element", first_payload)
        second = tools.materialize_blind_comparisons(self.iteration_dir, "create-element", second_payload)

        self.assertEqual(second["comparison_count"], 1)
        self.assertEqual(second["added_count"], 0)
        self.assertEqual(second["replaced_count"], 1)

        persisted = tools.read_json(self.iteration_dir / "create-element" / "blind-comparisons.json")
        self.assertEqual(persisted["comparisons"][0]["winner"], "B")
        self.assertEqual(persisted["comparisons"][0]["reasoning"], "Re-evaluated judgment.")

    def test_materialize_comparisons_parser_accepts_workspace_root_compat_flag(self) -> None:
        parser = tools.build_parser()

        args = parser.parse_args(
            [
                "materialize-comparisons",
                "--iteration",
                str(self.iteration_dir),
                "--skill",
                "create-element",
                "--raw-json",
                str(self.workspace_root / "raw-blind.json"),
                "--workspace-root",
                str(self.workspace_root),
            ]
        )

        self.assertEqual(args.workspace_root, self.workspace_root)

    def test_blind_compare_bundle_includes_ack_schema_hint(self) -> None:
        blind_dir = self.iteration_dir / "create-element" / "eval-0" / "blind" / "run-1"
        blind_dir.mkdir(parents=True, exist_ok=True)
        (blind_dir / "A.md").write_text("A\n", encoding="utf-8")
        (blind_dir / "B.md").write_text("B\n", encoding="utf-8")

        bundle = tools.build_blind_compare_bundle(self.iteration_dir, self.workspace_root, "create-element", 0, 1)

        self.assertEqual(bundle["ack_schema_hint"]["eval_id"], 0)
        self.assertEqual(bundle["ack_schema_hint"]["run_number"], 1)
        self.assertEqual(bundle["ack_schema_hint"]["winner"], "A | B | TIE")
        self.assertIn("raw_json_path", bundle["ack_schema_hint"])

    def test_read_json_reports_path_and_context_for_invalid_json(self) -> None:
        bad_path = self.workspace_root / "broken.json"
        bad_path.write_text('{"a": 1 trailing}\n', encoding="utf-8")

        with self.assertRaises(ValueError) as context:
            tools.read_json(bad_path)

        message = str(context.exception)
        self.assertIn(str(bad_path), message)
        self.assertIn("Invalid JSON", message)
        self.assertIn("Context:", message)

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

    def test_default_protocol_version_is_benchmark_v3(self) -> None:
        manifest = tools.build_protocol_manifest(self.workspace_root)

        self.assertEqual(manifest["protocol_version"], "benchmark-v3")

    def test_find_previous_iteration_supports_named_skill_series(self) -> None:
        series_root = self.workspace_root / "test"
        base = series_root / "likec4-dsl-test"
        second = series_root / "likec4-dsl-test2"
        third = series_root / "likec4-dsl-test3"
        unrelated = series_root / "other-skill-test4"
        for path in (base, second, third, unrelated):
            path.mkdir(parents=True, exist_ok=True)

        self.assertEqual(tools.find_previous_iteration(series_root, second), base)
        self.assertEqual(tools.find_previous_iteration(series_root, third), second)
        self.assertIsNone(tools.find_previous_iteration(series_root, base))

    def test_benchmark_agent_plan_defaults_to_parallel_within_phase(self) -> None:
        plan = tools.benchmark_agent_plan(self.iteration_dir, skill="create-element")

        self.assertEqual(plan["parallelism"]["default_policy"], "parallel-within-phase")
        self.assertEqual(plan["parallelism"]["cross_phase_parallelism"], "forbidden")
        self.assertEqual(plan["parallelism"]["unit_of_parallelism"], "<skill, eval_id, configuration, run_number>")

        phases = {entry["phase"]: entry for entry in plan["phases"]}
        self.assertEqual(phases["without_skill"]["dispatch_mode"], "parallel")
        self.assertEqual(phases["with_skill"]["dispatch_mode"], "parallel")
        self.assertEqual(phases["blind_compare"]["dispatch_mode"], "parallel")
        self.assertEqual(phases["without_skill"]["parallel_scope"], "<skill, eval_id, run_number>")
        self.assertEqual(phases["with_skill"]["parallel_scope"], "<skill, eval_id, run_number>")

        self.assertTrue(
            any("parallel within each phase" in note for note in plan.get("notes", []))
        )

    def test_materialize_run_aggregates_parallel_eval_workers_into_one_config_run(self) -> None:
        self._write_two_eval_split_evals("create-element")
        raw_eval_0 = self._write_json(
            self.workspace_root / "parallel-eval-0.json",
            {
                "skill_name": "create-element",
                "configuration": "with_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:00:00Z",
                "finished_at": "2026-03-13T10:00:03Z",
                "responses": [{"id": 0, "response": "API answer"}],
            },
        )
        raw_eval_1 = self._write_json(
            self.workspace_root / "parallel-eval-1.json",
            {
                "skill_name": "create-element",
                "configuration": "with_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:00:01Z",
                "finished_at": "2026-03-13T10:00:05Z",
                "responses": [{"id": 1, "response": "Webapp answer"}],
            },
        )

        first = tools.materialize_run_artifacts(self.iteration_dir, "create-element", "with_skill", raw_eval_0, run_number=1)
        second = tools.materialize_run_artifacts(self.iteration_dir, "create-element", "with_skill", raw_eval_1, run_number=1)

        self.assertIsNotNone(first["per_eval_metrics_path"])
        self.assertIsNotNone(second["per_eval_metrics_path"])

        summary = tools.summarize_config(
            self.iteration_dir / "create-element",
            "with_skill",
            self.workspace_root / ".github" / "skills" / "create-element" / "evals" / "evals-public.json",
        )

        self.assertEqual(summary["run_count"], 1)
        self.assertEqual(len(summary["runs"]), 1)
        self.assertEqual(len(summary["runs"][0]["evals"]), 2)
        self.assertEqual(summary["summary"]["elapsed_seconds_total"], 7.0)
        self.assertTrue((self.iteration_dir / "create-element" / "_runs" / "with_skill" / "run-1" / "eval-0-metrics.json").exists())
        self.assertTrue((self.iteration_dir / "create-element" / "_runs" / "with_skill" / "run-1" / "eval-1-metrics.json").exists())

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

    def test_materialize_run_uses_per_response_timestamps_when_top_level_missing(self) -> None:
        raw_payload = self._write_json(
            self.workspace_root / "run-per-response-timing.json",
            {
                "skill_name": "create-element",
                "configuration": "with_skill",
                "language": "English",
                "mcp_used": False,
                "responses": [
                    {
                        "id": 0,
                        "response": "timed response",
                        "started_at": "2026-03-13T10:00:00Z",
                        "finished_at": "2026-03-13T10:00:07Z",
                    }
                ],
            },
        )

        summary = tools.materialize_run_artifacts(
            self.iteration_dir,
            "create-element",
            "with_skill",
            raw_payload,
            run_number=1,
        )

        self.assertEqual(summary["elapsed_seconds_total"], 7.0)
        metrics = tools.read_json(self.iteration_dir / "create-element" / "with_skill-run-metrics.json")
        self.assertEqual(metrics["started_at"], "2026-03-13T10:00:00Z")
        self.assertEqual(metrics["finished_at"], "2026-03-13T10:00:07Z")

    def test_cmd_summarize_config_supports_legacy_iteration_skill_arguments(self) -> None:
        skill_dir = self.iteration_dir / "create-element"
        response_path = skill_dir / "eval-0" / "with_skill" / "run-1" / "response.md"
        response_path.parent.mkdir(parents=True, exist_ok=True)
        response_path.write_text("legacy summarize command response\n", encoding="utf-8")

        self._write_json(
            skill_dir / "with_skill-run-metrics.json",
            {
                "skill_name": "create-element",
                "configuration": "with_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:00:00Z",
                "finished_at": "2026-03-13T10:00:05Z",
                "elapsed_seconds_total": 5.0,
                "files_read_count": 1,
                "files_written_count": 1,
                "run_count": 1,
                "runs": [
                    {
                        "skill_name": "create-element",
                        "configuration": "with_skill",
                        "language": "English",
                        "mcp_used": False,
                        "started_at": "2026-03-13T10:00:00Z",
                        "finished_at": "2026-03-13T10:00:05Z",
                        "elapsed_seconds_total": 5.0,
                        "files_read_count": 1,
                        "files_written_count": 1,
                        "run_number": 1,
                    }
                ],
                "aggregate": {},
            },
        )

        parser = tools.build_parser()
        args = parser.parse_args(
            [
                "summarize-config",
                "--iteration",
                str(self.iteration_dir),
                "--skill",
                "create-element",
                "--config",
                "with_skill",
                "--workspace-root",
                str(self.workspace_root),
            ]
        )
        args.iteration = args.iteration.resolve()
        args.workspace_root = args.workspace_root.resolve()
        args.func(args)

        summary_path = skill_dir / "with_skill-summary.json"
        self.assertTrue(summary_path.exists())
        summary = tools.read_json(summary_path)
        self.assertEqual(summary["skill_name"], "create-element")
        self.assertEqual(summary["configuration"], "with_skill")

    def test_cmd_summarize_config_infers_evals_from_skill_dir_when_omitted(self) -> None:
        skill_dir = self.iteration_dir / "create-element"
        response_path = skill_dir / "eval-0" / "with_skill" / "run-1" / "response.md"
        response_path.parent.mkdir(parents=True, exist_ok=True)
        response_path.write_text("inferred evals response\n", encoding="utf-8")

        self._write_json(
            skill_dir / "with_skill-run-metrics.json",
            {
                "skill_name": "create-element",
                "configuration": "with_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:00:00Z",
                "finished_at": "2026-03-13T10:00:05Z",
                "elapsed_seconds_total": 5.0,
                "files_read_count": 1,
                "files_written_count": 1,
                "run_count": 1,
                "runs": [
                    {
                        "skill_name": "create-element",
                        "configuration": "with_skill",
                        "language": "English",
                        "mcp_used": False,
                        "started_at": "2026-03-13T10:00:00Z",
                        "finished_at": "2026-03-13T10:00:05Z",
                        "elapsed_seconds_total": 5.0,
                        "files_read_count": 1,
                        "files_written_count": 1,
                        "run_number": 1,
                    }
                ],
                "aggregate": {},
            },
        )

        parser = tools.build_parser()
        args = parser.parse_args(
            [
                "summarize-config",
                "--skill-dir",
                str(skill_dir),
                "--config",
                "with_skill",
                "--workspace-root",
                str(self.workspace_root),
            ]
        )
        args.workspace_root = args.workspace_root.resolve()
        args.func(args)

        summary_path = skill_dir / "with_skill-summary.json"
        self.assertTrue(summary_path.exists())
        summary = tools.read_json(summary_path)
        self.assertEqual(summary["skill_name"], "create-element")
        self.assertEqual(summary["configuration"], "with_skill")

    def test_refresh_run_metrics_collection_canonicalizes_alias_keys(self) -> None:
        skill_dir = self.iteration_dir / "create-element"
        metrics_path = skill_dir / "_runs" / "with_skill" / "run-1-metrics.json"
        self._write_json(
            metrics_path,
            {
                "skill_name": "create-element",
                "configuration": "with_skill",
                "language": "English",
                "mcp_used": False,
                "started_at_utc": "2026-03-13T10:00:00Z",
                "finished_at_utc": "2026-03-13T10:00:05Z",
                "elapsed_seconds_total": 5.0,
                "workspace_files_intentionally_read": 3,
                "files_written_under_target_output_dir_count": 1,
            },
        )

        collection = tools.refresh_run_metrics_collection(skill_dir, "with_skill")

        self.assertEqual(collection["started_at"], "2026-03-13T10:00:00Z")
        self.assertEqual(collection["finished_at"], "2026-03-13T10:00:05Z")
        self.assertEqual(collection["files_read_count"], 3)
        self.assertEqual(collection["files_written_count"], 1)
        self.assertNotIn("started_at_utc", collection["runs"][0])

    def test_refresh_suite_outputs_after_blind_writes_suite_summary_files(self) -> None:
        skill_dir = self.iteration_dir / "create-element"
        with_response = skill_dir / "eval-0" / "with_skill" / "response.md"
        without_response = skill_dir / "eval-0" / "without_skill" / "response.md"
        with_response.parent.mkdir(parents=True, exist_ok=True)
        without_response.parent.mkdir(parents=True, exist_ok=True)
        with_response.write_text("with skill answer\n", encoding="utf-8")
        without_response.write_text("without skill answer\n", encoding="utf-8")

        self._write_json(
            skill_dir / "with_skill-run-metrics.json",
            {
                "skill_name": "create-element",
                "configuration": "with_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:00:00Z",
                "finished_at": "2026-03-13T10:00:05Z",
                "elapsed_seconds_total": 5.0,
                "files_read_count": 1,
                "files_written_count": 1,
            },
        )
        self._write_json(
            skill_dir / "without_skill-run-metrics.json",
            {
                "skill_name": "create-element",
                "configuration": "without_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:01:00Z",
                "finished_at": "2026-03-13T10:01:08Z",
                "elapsed_seconds_total": 8.0,
                "files_read_count": 0,
                "files_written_count": 1,
            },
        )

        self._write_json(skill_dir / "eval-0" / "blind-map.run-1.json", {"A": "with_skill", "B": "without_skill"})
        self._write_json(
            skill_dir / "blind-comparisons.json",
            {
                "schema_version": 2,
                "skill_name": "create-element",
                "comparisons": [
                    {
                        "schema_version": 2,
                        "eval_id": 0,
                        "run_number": 1,
                        "winner": "A",
                        "reasoning": "A is better.",
                        "rubric": {
                            "A": {"content_score": 9, "structure_score": 9, "overall_score": 9},
                            "B": {"content_score": 5, "structure_score": 5, "overall_score": 5},
                        },
                        "expectation_results": {
                            "A": {"passed": 2, "total": 2, "pass_rate": 1.0},
                            "B": {"passed": 1, "total": 2, "pass_rate": 0.5},
                        },
                    }
                ],
            },
        )

        refresh = tools.refresh_suite_outputs_after_blind(self.iteration_dir, self.workspace_root, "create-element")

        suite_json = self.iteration_dir / "suite-summary.json"
        suite_md = self.iteration_dir / "suite-summary.md"
        self.assertTrue(suite_json.exists())
        self.assertTrue(suite_md.exists())
        self.assertEqual(refresh["skill_count"], 1)
        suite = tools.read_json(suite_json)
        self.assertEqual(suite["skill_count"], 1)
        self.assertEqual(suite["overview"][0]["skill"], "create-element")

    def test_pre_aggregate_check_fails_when_blind_comparisons_missing(self) -> None:
        skill_dir = self.iteration_dir / "create-element"
        for filename in (
            "with_skill-run-metrics.json",
            "without_skill-run-metrics.json",
            "with_skill-summary.json",
            "without_skill-summary.json",
        ):
            self._write_json(
                skill_dir / filename,
                {
                    "skill_name": "create-element",
                    "configuration": "with_skill" if filename.startswith("with") else "without_skill",
                    "language": "English",
                    "mcp_used": False,
                    "started_at": "2026-03-13T10:00:00Z",
                    "finished_at": "2026-03-13T10:00:05Z",
                    "elapsed_seconds_total": 5.0,
                    "files_read_count": 1,
                    "files_written_count": 1,
                    "run_count": 1,
                    "runs": [
                        {
                            "skill_name": "create-element",
                            "configuration": "with_skill" if filename.startswith("with") else "without_skill",
                            "language": "English",
                            "mcp_used": False,
                            "started_at": "2026-03-13T10:00:00Z",
                            "finished_at": "2026-03-13T10:00:05Z",
                            "elapsed_seconds_total": 5.0,
                            "files_read_count": 1,
                            "files_written_count": 1,
                            "run_number": 1,
                        }
                    ],
                    "aggregate": {},
                    "summary": {},
                    "variance": {},
                    "evals": [],
                    "high_variance_evals": [],
                },
            )

        summary = tools.pre_aggregate_check(self.iteration_dir, self.workspace_root)

        self.assertEqual(summary["status"], "fail")
        self.assertEqual(summary["issue_count"], 1)
        self.assertEqual(summary["issues"][0]["file"], "blind-comparisons.json")

    def test_pre_aggregate_check_fails_when_blind_comparisons_do_not_cover_all_prepared_runs(self) -> None:
        skill_dir = self.iteration_dir / "create-element"

        for filename, configuration in (
            ("with_skill-run-metrics.json", "with_skill"),
            ("without_skill-run-metrics.json", "without_skill"),
        ):
            self._write_json(
                skill_dir / filename,
                {
                    "skill_name": "create-element",
                    "configuration": configuration,
                    "language": "English",
                    "mcp_used": False,
                    "started_at": "2026-03-13T10:00:00Z",
                    "finished_at": "2026-03-13T10:00:05Z",
                    "elapsed_seconds_total": 5.0,
                    "files_read_count": 1,
                    "files_written_count": 1,
                    "run_count": 1,
                    "runs": [
                        {
                            "skill_name": "create-element",
                            "configuration": configuration,
                            "language": "English",
                            "mcp_used": False,
                            "started_at": "2026-03-13T10:00:00Z",
                            "finished_at": "2026-03-13T10:00:05Z",
                            "elapsed_seconds_total": 5.0,
                            "files_read_count": 1,
                            "files_written_count": 1,
                            "run_number": 1,
                        }
                    ],
                    "aggregate": {},
                },
            )

        self._write_json(skill_dir / "with_skill-summary.json", {"summary": {}, "evals": []})
        self._write_json(skill_dir / "without_skill-summary.json", {"summary": {}, "evals": []})

        blind_run_1 = skill_dir / "eval-0" / "blind" / "run-1"
        blind_run_1.mkdir(parents=True, exist_ok=True)
        (blind_run_1 / "A.md").write_text("A1\n", encoding="utf-8")
        (blind_run_1 / "B.md").write_text("B1\n", encoding="utf-8")
        self._write_json(skill_dir / "eval-0" / "blind-map.run-1.json", {"A": "with_skill", "B": "without_skill"})

        blind_run_2 = skill_dir / "eval-0" / "blind" / "run-2"
        blind_run_2.mkdir(parents=True, exist_ok=True)
        (blind_run_2 / "A.md").write_text("A2\n", encoding="utf-8")
        (blind_run_2 / "B.md").write_text("B2\n", encoding="utf-8")
        self._write_json(skill_dir / "eval-0" / "blind-map.run-2.json", {"A": "without_skill", "B": "with_skill"})

        self._write_json(
            skill_dir / "blind-comparisons.json",
            {
                "schema_version": 2,
                "skill_name": "create-element",
                "comparisons": [
                    {
                        "schema_version": 2,
                        "eval_id": 0,
                        "run_number": 1,
                        "winner": "A",
                        "reasoning": "Run 1 judged.",
                        "rubric": {
                            "A": {"content_score": 8, "structure_score": 8, "overall_score": 8},
                            "B": {"content_score": 6, "structure_score": 6, "overall_score": 6},
                        },
                        "expectation_results": {
                            "A": {"passed": 2, "total": 2, "pass_rate": 1.0},
                            "B": {"passed": 1, "total": 2, "pass_rate": 0.5},
                        },
                    }
                ],
            },
        )

        summary = tools.pre_aggregate_check(self.iteration_dir, self.workspace_root)

        self.assertEqual(summary["status"], "fail")
        self.assertEqual(summary["issue_count"], 1)
        self.assertEqual(summary["issues"][0]["reason"], "missing-blind-comparisons-for-prepared-runs")
        self.assertEqual(summary["issues"][0]["details"]["expected_count"], 2)
        self.assertEqual(summary["issues"][0]["details"]["actual_count"], 1)

    def test_resume_finalize_materializes_missing_blind_comparisons_from_meta(self) -> None:
        skill_dir = self.iteration_dir / "create-element"
        with_response = skill_dir / "eval-0" / "with_skill" / "response.md"
        without_response = skill_dir / "eval-0" / "without_skill" / "response.md"
        with_response.parent.mkdir(parents=True, exist_ok=True)
        without_response.parent.mkdir(parents=True, exist_ok=True)
        with_response.write_text("with skill answer\n", encoding="utf-8")
        without_response.write_text("without skill answer\n", encoding="utf-8")

        self._write_json(
            skill_dir / "with_skill-run-metrics.json",
            {
                "skill_name": "create-element",
                "configuration": "with_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:00:00Z",
                "finished_at": "2026-03-13T10:00:05Z",
                "elapsed_seconds_total": 5.0,
                "files_read_count": 1,
                "files_written_count": 1,
                "run_count": 1,
                "runs": [
                    {
                        "skill_name": "create-element",
                        "configuration": "with_skill",
                        "language": "English",
                        "mcp_used": False,
                        "started_at": "2026-03-13T10:00:00Z",
                        "finished_at": "2026-03-13T10:00:05Z",
                        "elapsed_seconds_total": 5.0,
                        "files_read_count": 1,
                        "files_written_count": 1,
                        "run_number": 1,
                    }
                ],
                "aggregate": {},
            },
        )
        self._write_json(
            skill_dir / "without_skill-run-metrics.json",
            {
                "skill_name": "create-element",
                "configuration": "without_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:01:00Z",
                "finished_at": "2026-03-13T10:01:08Z",
                "elapsed_seconds_total": 8.0,
                "files_read_count": 0,
                "files_written_count": 1,
                "run_count": 1,
                "runs": [
                    {
                        "skill_name": "create-element",
                        "configuration": "without_skill",
                        "language": "English",
                        "mcp_used": False,
                        "started_at": "2026-03-13T10:01:00Z",
                        "finished_at": "2026-03-13T10:01:08Z",
                        "elapsed_seconds_total": 8.0,
                        "files_read_count": 0,
                        "files_written_count": 1,
                        "run_number": 1,
                    }
                ],
                "aggregate": {},
            },
        )
        self._write_json(skill_dir / "eval-0" / "blind-map.run-1.json", {"A": "with_skill", "B": "without_skill"})

        evals_path = self.workspace_root / ".github" / "skills" / "create-element" / "evals" / "evals-public.json"
        tools.summarize_config(skill_dir, "with_skill", evals_path)
        tools.summarize_config(skill_dir, "without_skill", evals_path)

        self._write_json(
            self.iteration_dir / "_meta" / "create-element-blind.json",
            {
                "skill_name": "create-element",
                "comparisons": [
                    {
                        "eval_id": 0,
                        "run_number": 1,
                        "winner": "A",
                        "reasoning": "A is better.",
                        "rubric": {
                            "A": {"content_score": 9, "structure_score": 9, "overall_score": 9},
                            "B": {"content_score": 5, "structure_score": 5, "overall_score": 5},
                        },
                        "expectation_results": {
                            "A": {"passed": 2, "total": 2, "pass_rate": 1.0},
                            "B": {"passed": 1, "total": 2, "pass_rate": 0.5},
                        },
                    }
                ],
            },
        )

        result = tools.resume_finalize_iteration(self.iteration_dir, self.workspace_root)

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["materialized_count"], 1)
        self.assertTrue((skill_dir / "blind-comparisons.json").exists())
        self.assertTrue((self.iteration_dir / "suite-summary.json").exists())
        self.assertTrue((self.iteration_dir / "suite-summary.md").exists())

    def test_resume_finalize_blocks_when_blind_comparisons_cannot_be_materialized(self) -> None:
        skill_dir = self.iteration_dir / "create-element"
        skill_dir.mkdir(parents=True, exist_ok=True)

        result = tools.resume_finalize_iteration(self.iteration_dir, self.workspace_root)

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["materialized_count"], 0)
        self.assertEqual(result["unresolved_count"], 1)
        self.assertEqual(result["unresolved"][0]["skill"], "create-element")

    def test_aggregate_suite_reports_skipped_skills_explicitly(self) -> None:
        second_skill = "create-relationship"
        self._write_split_evals(second_skill)

        good_skill_dir = self.iteration_dir / "create-element"
        with_response = good_skill_dir / "eval-0" / "with_skill" / "response.md"
        without_response = good_skill_dir / "eval-0" / "without_skill" / "response.md"
        with_response.parent.mkdir(parents=True, exist_ok=True)
        without_response.parent.mkdir(parents=True, exist_ok=True)
        with_response.write_text("with skill answer\n", encoding="utf-8")
        without_response.write_text("without skill answer\n", encoding="utf-8")

        self._write_json(
            good_skill_dir / "with_skill-run-metrics.json",
            {
                "skill_name": "create-element",
                "configuration": "with_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:00:00Z",
                "finished_at": "2026-03-13T10:00:05Z",
                "elapsed_seconds_total": 5.0,
                "files_read_count": 1,
                "files_written_count": 1,
            },
        )
        self._write_json(
            good_skill_dir / "without_skill-run-metrics.json",
            {
                "skill_name": "create-element",
                "configuration": "without_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:01:00Z",
                "finished_at": "2026-03-13T10:01:08Z",
                "elapsed_seconds_total": 8.0,
                "files_read_count": 0,
                "files_written_count": 1,
            },
        )
        self._write_json(good_skill_dir / "eval-0" / "blind-map.run-1.json", {"A": "with_skill", "B": "without_skill"})
        self._write_json(
            good_skill_dir / "blind-comparisons.json",
            {
                "schema_version": 2,
                "skill_name": "create-element",
                "comparisons": [
                    {
                        "schema_version": 2,
                        "eval_id": 0,
                        "run_number": 1,
                        "winner": "A",
                        "reasoning": "A is better.",
                        "rubric": {
                            "A": {"content_score": 9, "structure_score": 9, "overall_score": 9},
                            "B": {"content_score": 5, "structure_score": 5, "overall_score": 5},
                        },
                        "expectation_results": {
                            "A": {"passed": 2, "total": 2, "pass_rate": 1.0},
                            "B": {"passed": 1, "total": 2, "pass_rate": 0.5},
                        },
                    }
                ],
            },
        )
        evals_path = self.workspace_root / ".github" / "skills" / "create-element" / "evals" / "evals-public.json"
        tools.summarize_config(good_skill_dir, "with_skill", evals_path)
        tools.summarize_config(good_skill_dir, "without_skill", evals_path)

        skipped_skill_dir = self.iteration_dir / second_skill
        skipped_skill_dir.mkdir(parents=True, exist_ok=True)

        suite = tools.aggregate_suite(self.iteration_dir, self.workspace_root)

        self.assertEqual(suite["skill_count"], 1)
        self.assertEqual(len(suite["skipped_skills"]), 1)
        self.assertEqual(suite["skipped_skills"][0]["skill"], second_skill)
        self.assertIn("missing required artifacts", suite["skipped_skills"][0]["reason"])

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

    def test_extract_likec4_snippets_balances_unfenced_blocks_without_orphan_braces(self) -> None:
        response_text = (
            "Here is the model.\n\n"
            "model {\n"
            "  frontend = service 'Frontend' {\n"
            "  }\n"
            "  db = database 'DB'\n"
            "  frontend -> db 'reads'\n"
            "}\n\n"
            "And the deployment.\n\n"
            "deployment {\n"
            "  liveFrontend instanceOf frontend\n"
            "}\n"
        )

        snippets = tools.extract_likec4_snippets(response_text)

        self.assertEqual(len(snippets), 2)
        self.assertFalse(any(snippet.strip() == "}" for snippet in snippets))
        self.assertTrue(any("frontend -> db 'reads'" in snippet for snippet in snippets))

    def test_analyze_likec4_response_accepts_generic_kinds_instanceof_and_dynamic_chain(self) -> None:
        response_text = (
            "model {\n"
            "  monitor = system 'Monitor'\n"
            "  cloud = system 'Cloud' {\n"
            "    backend = container 'Backend'\n"
            "  }\n"
            "  liveBackend instanceOf cloud.backend\n"
            "  monitor -[calls]-> cloud.backend 'observes'\n"
            "}\n\n"
            "views {\n"
            "  dynamic monitorFlow {\n"
            "    include *\n"
            "    monitor -> cloud -> cloud.backend\n"
            "  }\n"
            "}\n"
        )

        analysis = tools.analyze_likec4_response(response_text, tools.load_likec4_reference_data(self.workspace_root))

        self.assertEqual(analysis["status"], "checked")
        self.assertEqual(analysis["error_count"], 0)
        self.assertGreaterEqual(analysis["snippet_count"], 1)

    def test_iteration_caveats_flag_provisional_comparison(self) -> None:
        validity = tools.derive_iteration_comparison_validity(
            {
                "reused_blind_comparisons_from_iteration": "iteration-4",
                "synthetic_timing": True,
                "with_skill_guidance_injected": True,
                "notes": ["documented fallback"],
            }
        )

        self.assertTrue(validity["provisional"])
        self.assertFalse(validity["blind_metrics_trustworthy"])
        self.assertFalse(validity["time_metrics_trustworthy"])
        self.assertFalse(validity["previous_iteration_comparison_trustworthy"])
        self.assertTrue(validity["reasons"])
        self.assertTrue(validity["protocol_deviations"])

    def test_apply_iteration_comparison_validity_masks_untrustworthy_metrics(self) -> None:
        skill_rows = [
            {
                "skill": "create-element",
                "capability": {
                    "blind": {
                        "with_skill_win_rate": 0.8,
                        "without_skill_win_rate": 0.2,
                        "variance": {
                            "with_skill_win_rate": {"mean": 0.8},
                            "without_skill_win_rate": {"mean": 0.2},
                        },
                    },
                    "expectation_pass_rate": {
                        "with_skill": 0.9,
                        "without_skill": 0.7,
                        "delta": 0.2,
                        "variance": {
                            "with_skill": {"mean": 0.9},
                            "without_skill": {"mean": 0.7},
                            "delta": {"mean": 0.2},
                        },
                    },
                    "rubric_score": {
                        "with_skill": 8.5,
                        "without_skill": 7.0,
                        "delta": 1.5,
                        "variance": {
                            "with_skill": {"mean": 8.5},
                            "without_skill": {"mean": 7.0},
                            "delta": {"mean": 1.5},
                        },
                    },
                    "high_variance_evals": [{"id": 0, "source": "blind"}],
                },
                "time": {
                    "with_skill": {
                        "elapsed_seconds_total": 12.0,
                        "elapsed_seconds_per_eval": 3.0,
                        "variance": {
                            "elapsed_seconds_total": {"mean": 12.0},
                            "elapsed_seconds_per_eval": {"mean": 3.0},
                            "response_words_total": {"mean": 120.0},
                            "response_words_per_eval": {"mean": 30.0},
                            "files_read_count": {"mean": 2.0},
                            "files_written_count": {"mean": 4.0},
                        },
                    },
                    "without_skill": {
                        "elapsed_seconds_total": 20.0,
                        "elapsed_seconds_per_eval": 5.0,
                        "variance": {
                            "elapsed_seconds_total": {"mean": 20.0},
                            "elapsed_seconds_per_eval": {"mean": 5.0},
                            "response_words_total": {"mean": 150.0},
                            "response_words_per_eval": {"mean": 37.5},
                            "files_read_count": {"mean": 1.0},
                            "files_written_count": {"mean": 4.0},
                        },
                    },
                    "delta": {
                        "elapsed_seconds_total": -8.0,
                        "elapsed_seconds_per_eval": -2.0,
                    },
                },
                "high_variance_evals": [{"source": "blind", "id": 0}, {"source": "with_skill", "id": 1}],
            }
        ]

        tools.apply_iteration_comparison_validity(
            skill_rows,
            {
                "blind_metrics_trustworthy": False,
                "time_metrics_trustworthy": False,
            },
        )

        masked = skill_rows[0]
        self.assertIsNone(masked["capability"]["blind"]["with_skill_win_rate"])
        self.assertIsNone(masked["capability"]["expectation_pass_rate"]["delta"])
        self.assertIsNone(masked["capability"]["rubric_score"]["with_skill"])
        self.assertEqual(masked["capability"]["high_variance_evals"], [])
        self.assertEqual(masked["high_variance_evals"], [{"source": "with_skill", "id": 1}])
        self.assertIsNone(masked["time"]["with_skill"]["elapsed_seconds_total"])
        self.assertIsNone(masked["time"]["delta"]["elapsed_seconds_per_eval"])

    def test_clean_benchmark_artifacts_removes_iterations_and_disposables(self) -> None:
        (self.workspace_root / "test" / "iteration-1" / "foo").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "test" / "iteration-2" / "bar").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "test" / "likec4-dsl-test4" / "baz").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "test" / "_agent-hooks").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "test" / "_live-mcp-probe").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "test" / "scripts" / "__pycache__").mkdir(parents=True, exist_ok=True)

        summary = tools.clean_benchmark_artifacts(self.workspace_root)

        self.assertEqual(summary["removed_count"], 7)
        self.assertFalse((self.workspace_root / "test" / "iteration-1").exists())
        self.assertFalse((self.workspace_root / "test" / "iteration-2").exists())
        self.assertFalse((self.workspace_root / "test" / "iteration-9").exists())
        self.assertFalse((self.workspace_root / "test" / "likec4-dsl-test4").exists())
        self.assertFalse((self.workspace_root / "test" / "_agent-hooks").exists())
        self.assertFalse((self.workspace_root / "test" / "_live-mcp-probe").exists())
        self.assertFalse((self.workspace_root / "test" / "scripts" / "__pycache__").exists())
        self.assertTrue((self.workspace_root / "test" / "_meta" / "clean-benchmark-artifacts.json").exists())

    def test_prune_generated_artifacts_removes_review_exports_only(self) -> None:
        skill_dir = self.iteration_dir / "create-element"
        review_workspace = skill_dir / "_skill-creator-review-workspace"
        review_workspace.mkdir(parents=True, exist_ok=True)
        benchmark_json = skill_dir / "skill-creator-benchmark.json"
        review_html = skill_dir / "skill-creator-review.html"
        retained_summary = self.iteration_dir / "suite-summary.json"
        retained_summary.parent.mkdir(parents=True, exist_ok=True)

        benchmark_json.write_text("{}\n", encoding="utf-8")
        review_html.write_text("<html></html>\n", encoding="utf-8")
        retained_summary.write_text("{}\n", encoding="utf-8")

        summary = tools.prune_generated_artifacts(self.iteration_dir, self.workspace_root)

        self.assertEqual(summary["removed_count"], 3)
        self.assertFalse(review_workspace.exists())
        self.assertFalse(benchmark_json.exists())
        self.assertFalse(review_html.exists())
        self.assertTrue(retained_summary.exists())
        self.assertTrue((self.iteration_dir / "_meta" / "generated-artifacts-pruned.json").exists())

    def test_trace_level_defaults_to_off_and_supports_audit_and_debug(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(resolve_trace_level(), "off")
            self.assertIsNone(resolve_audit_log_path(self.workspace_root))

        with patch.dict("os.environ", {"BENCH_TRACE_LEVEL": "audit"}, clear=True):
            self.assertEqual(resolve_trace_level(), "audit")
            self.assertEqual(
                resolve_audit_log_path(self.workspace_root),
                self.workspace_root / "test" / "_agent-hooks" / "hook-audit.jsonl",
            )

        with patch.dict("os.environ", {"BENCH_TRACE_LEVEL": "debug", "BENCH_DEBUG_LOG": "test/_agent-hooks/hook-debug.jsonl"}, clear=True):
            self.assertEqual(resolve_trace_level(), "debug")
            self.assertEqual(
                resolve_audit_log_path(self.workspace_root),
                self.workspace_root / "test" / "_agent-hooks" / "hook-audit.jsonl",
            )

    def test_trace_level_preserves_legacy_debug_hooks_compatibility(self) -> None:
        with patch.dict("os.environ", {"BENCH_DEBUG_HOOKS": "true", "BENCH_DEBUG_LOG": "test/_agent-hooks/custom-debug.jsonl"}, clear=True):
            self.assertEqual(resolve_trace_level(), "debug")
            self.assertEqual(
                resolve_audit_log_path(self.workspace_root),
                self.workspace_root / "test" / "_agent-hooks" / "hook-audit.jsonl",
            )

    def test_snapshot_public_evals_writes_iteration_meta_copy(self) -> None:
        summary = tools.snapshot_public_evals(self.iteration_dir, self.workspace_root)

        self.assertEqual(summary["skill_count"], 1)
        self.assertEqual(summary["skills"][0]["skill_name"], "create-element")
        self.assertEqual(summary["skills"][0]["evals"][0]["prompt"], "Add an API container.")
        self.assertTrue(summary["skills"][0]["worker_prompt_inputs"])
        prompt_paths = summary["skills"][0]["worker_prompt_inputs"][0]
        self.assertTrue((self.workspace_root / prompt_paths["prompt_md_path"]).exists())
        self.assertTrue((self.workspace_root / prompt_paths["prompt_json_path"]).exists())
        snapshot_path = self.iteration_dir / "_meta" / "evals-public-snapshot.json"
        self.assertTrue(snapshot_path.exists())

    def test_snapshot_public_evals_works_when_workspace_skills_are_relocated(self) -> None:
        skills_root = self.workspace_root / ".github" / "skills"
        disabled_root = self.iteration_dir / "_disabled-skills"
        disabled_root.mkdir(parents=True, exist_ok=True)

        moved_skill = skills_root / "create-element"
        moved_destination = disabled_root / "create-element"
        moved_skill.rename(moved_destination)

        summary = tools.snapshot_public_evals(self.iteration_dir, self.workspace_root)

        self.assertEqual(summary["skill_count"], 1)
        self.assertEqual(summary["skills"][0]["skill_name"], "create-element")
        prompt_paths = summary["skills"][0]["worker_prompt_inputs"][0]
        self.assertTrue((self.workspace_root / prompt_paths["prompt_md_path"]).exists())
        self.assertTrue((self.workspace_root / prompt_paths["prompt_json_path"]).exists())

    def test_disable_workspace_skills_moves_all_and_marks_strict_ready(self) -> None:
        (self.workspace_root / ".github" / "skills" / "create-relationship" / "SKILL.md").parent.mkdir(parents=True, exist_ok=True)
        (self.workspace_root / ".github" / "skills" / "create-relationship" / "SKILL.md").write_text("x\n", encoding="utf-8")

        summary = tools.disable_workspace_skills(self.workspace_root, self.iteration_dir)

        self.assertTrue(summary["strict_ready"])
        self.assertEqual(summary["remaining_skills_root_count"], 0)
        self.assertEqual(summary["remaining_skills_root"], [])
        self.assertEqual(tools.skill_directory_names(self.workspace_root / ".github" / "skills"), [])
        self.assertGreaterEqual(summary["moved_count"], 2)

    def test_restore_workspace_skills_accepts_already_restored_skills(self) -> None:
        summary_disable = tools.disable_workspace_skills(self.workspace_root, self.iteration_dir)
        moved_skill_names = [item["skill"] for item in summary_disable["moved"]]

        first_skill = moved_skill_names[0]
        backup_path = self.iteration_dir / "_disabled-skills" / first_skill
        destination_path = self.workspace_root / ".github" / "skills" / first_skill
        backup_path.rename(destination_path)

        summary_restore = tools.restore_workspace_skills(self.workspace_root, self.iteration_dir)

        self.assertIn(first_skill, summary_restore["already_restored"])
        self.assertEqual(summary_restore["already_restored_count"], 1)
        self.assertEqual(sorted(tools.skill_directory_names(self.workspace_root / ".github" / "skills")), sorted(moved_skill_names))

    def test_current_utc_timestamp_returns_iso8601_utc_string(self) -> None:
        payload = tools.current_utc_timestamp()

        self.assertIn("timestamp", payload)
        self.assertIsNotNone(tools.iso_to_datetime(payload["timestamp"]))
        self.assertTrue(payload["timestamp"].endswith("Z"))

    def test_derive_run_metrics_from_responses_uses_response_file_mtime_window(self) -> None:
        skill_dir = self.iteration_dir / "create-element"
        response_0 = skill_dir / "eval-0" / "with_skill" / "run-2" / "response.md"
        response_1 = skill_dir / "eval-1" / "with_skill" / "run-2" / "response.md"
        response_0.parent.mkdir(parents=True, exist_ok=True)
        response_1.parent.mkdir(parents=True, exist_ok=True)
        response_0.write_text("answer 0\n", encoding="utf-8")
        response_1.write_text("answer 1\n", encoding="utf-8")

        t0 = 1773396000  # 2026-03-12T10:00:00Z
        t1 = 1773396009  # 2026-03-12T10:00:09Z
        os.utime(response_0, (t0, t0))
        os.utime(response_1, (t1, t1))

        summary = tools.derive_run_metrics_from_responses(
            self.iteration_dir,
            "create-element",
            "with_skill",
            2,
        )

        self.assertEqual(summary["responses_used"], 2)
        self.assertEqual(summary["elapsed_seconds_total"], 9.0)
        metrics = tools.read_json(skill_dir / "_runs" / "with_skill" / "run-2-metrics.json")
        self.assertEqual(metrics["run_number"], 2)
        self.assertEqual(metrics["files_written_count"], 2)
        self.assertEqual(metrics["elapsed_seconds_total"], 9.0)

    def test_validate_hook_audit_accepts_denied_broad_mcp_and_prompt_input_reads(self) -> None:
        audit_path = self.workspace_root / "test" / "_agent-hooks" / "hook-audit.jsonl"
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit_path.write_text(
            "\n".join(
                [
                    json.dumps(
                        {
                            "timestamp": "2026-03-16T21:00:00Z",
                            "mode": "baseline",
                            "tool_name": "read_file",
                            "tool_paths": ["test/likec4-dsl-test4/likec4-dsl/eval-4/input/prompt.md"],
                            "permissionDecision": "allow",
                        }
                    ),
                    json.dumps(
                        {
                            "timestamp": "2026-03-16T21:00:01Z",
                            "mode": "baseline",
                            "tool_name": "mcp_likec4_list-projects",
                            "tool_paths": [],
                            "permissionDecision": "deny",
                        }
                    ),
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        summary = tools.validate_hook_audit(audit_path, mode="baseline")

        self.assertTrue(summary["passed"])
        self.assertEqual(summary["issue_count"], 0)

    def test_validate_hook_audit_returns_not_enabled_when_file_is_missing(self) -> None:
        summary = tools.validate_hook_audit(self.workspace_root / "test" / "_agent-hooks" / "missing.jsonl", mode="baseline")

        self.assertTrue(summary["passed"])
        self.assertEqual(summary["status"], "not_enabled")
        self.assertEqual(summary["issue_count"], 0)

    def test_validate_hook_audit_flags_allowed_read_outside_baseline_scope(self) -> None:
        audit_path = self.workspace_root / "test" / "_agent-hooks" / "hook-audit.jsonl"
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit_path.write_text(
            json.dumps(
                {
                    "timestamp": "2026-03-16T21:00:00Z",
                    "mode": "baseline",
                    "tool_name": "read_file",
                    "tool_paths": ["projects/template/system-model.c4"],
                    "permissionDecision": "allow",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        summary = tools.validate_hook_audit(audit_path, mode="baseline")

        self.assertFalse(summary["passed"])
        self.assertEqual(summary["issue_count"], 1)
        self.assertEqual(summary["issues"][0]["problem"], "allowed-read-outside-mode-scope")

    def test_validate_hook_audit_accepts_baseline_prompt_input_reads(self) -> None:
        audit_path = self.workspace_root / "test" / "_agent-hooks" / "hook-audit.jsonl"
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit_path.write_text(
            json.dumps(
                {
                    "timestamp": "2026-03-16T21:00:00Z",
                    "mode": "baseline",
                    "tool_name": "read_file",
                    "tool_paths": ["test/likec4-dsl-test4/likec4-dsl/eval-4/input/prompt.md"],
                    "permissionDecision": "allow",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        summary = tools.validate_hook_audit(audit_path, mode="baseline")

        self.assertTrue(summary["passed"])
        self.assertEqual(summary["issue_count"], 0)

    def test_validate_hook_audit_reports_malformed_jsonl_lines_without_crashing(self) -> None:
        audit_path = self.workspace_root / "test" / "_agent-hooks" / "hook-audit.jsonl"
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit_path.write_text(
            "\n".join(
                [
                    json.dumps(
                        {
                            "timestamp": "2026-03-16T21:00:00Z",
                            "mode": "with_skill_targeted",
                            "tool_name": "read_file",
                            "tool_paths": [".github/skills/create-element/SKILL.md"],
                            "permissionDecision": "allow",
                        }
                    ),
                    "}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        summary = tools.validate_hook_audit(audit_path, mode="with_skill_targeted")

        self.assertFalse(summary["passed"])
        self.assertEqual(summary["entry_count"], 1)
        self.assertEqual(summary["malformed_line_count"], 1)
        self.assertEqual(summary["issue_count"], 1)
        self.assertEqual(summary["issues"][0]["problem"], "malformed-jsonl-line")
        self.assertEqual(summary["issues"][0]["line_number"], 2)
        self.assertEqual(summary["issues"][0]["raw_preview"], "}")

    def test_load_jsonl_records_stays_strict_for_malformed_jsonl_lines(self) -> None:
        audit_path = self.workspace_root / "test" / "_agent-hooks" / "hook-audit.jsonl"
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit_path.write_text("}\n", encoding="utf-8")

        with self.assertRaises(ValueError):
            tools.load_jsonl_records(audit_path)

    def test_reset_hook_state_removes_anonymous_targeted_and_legacy_default_files(self) -> None:
        hook_root = self.workspace_root / "test" / "_agent-hooks"
        hook_root.mkdir(parents=True, exist_ok=True)
        (hook_root / "anonymous-with_skill_targeted.json").write_text("{}\n", encoding="utf-8")
        (hook_root / "default.json").write_text("{}\n", encoding="utf-8")

        summary = tools.reset_hook_state(self.workspace_root, mode="with_skill_targeted")

        self.assertEqual(summary["resolved_session_ids"], ["anonymous-with_skill_targeted", "default"])
        self.assertEqual(summary["removed_count"], 2)
        self.assertIn("test/_agent-hooks/anonymous-with_skill_targeted.json", summary["removed"])
        self.assertIn("test/_agent-hooks/default.json", summary["removed"])
        self.assertFalse((hook_root / "anonymous-with_skill_targeted.json").exists())
        self.assertFalse((hook_root / "default.json").exists())

    def test_reset_hook_state_removes_derived_anonymous_state_files(self) -> None:
        hook_root = self.workspace_root / "test" / "_agent-hooks"
        hook_root.mkdir(parents=True, exist_ok=True)
        (hook_root / "anonymous-blind_compare-iteration-2-create-element.json").write_text("{}\n", encoding="utf-8")
        (hook_root / "anonymous-blind_compare-iteration-3-create-element.json").write_text("{}\n", encoding="utf-8")
        (hook_root / "default.json").write_text("{}\n", encoding="utf-8")

        summary = tools.reset_hook_state(self.workspace_root, mode="blind_compare")

        self.assertEqual(summary["removed_count"], 3)
        self.assertIn("anonymous-blind_compare-iteration-2-create-element", summary["resolved_session_ids"])
        self.assertIn("anonymous-blind_compare-iteration-3-create-element", summary["resolved_session_ids"])
        self.assertFalse((hook_root / "anonymous-blind_compare-iteration-2-create-element.json").exists())
        self.assertFalse((hook_root / "anonymous-blind_compare-iteration-3-create-element.json").exists())
        self.assertFalse((hook_root / "default.json").exists())

    def test_collect_harness_noise_reports_denied_discovery_and_duplicate_raw_payloads(self) -> None:
        audit_path = self.workspace_root / "test" / "_agent-hooks" / "hook-audit.jsonl"
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit_path.write_text(
            json.dumps(
                {
                    "timestamp": "2026-03-16T21:00:00Z",
                    "mode": "benchmark_manager",
                    "tool_name": "grep_search",
                    "tool_paths": ["test/iteration-9/create-element/eval-0/input/prompt.md"],
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "broad discovery denied for benchmark manager",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        duplicate_payload = {
            "skill_name": "create-element",
            "comparisons": [
                {
                    "eval_id": 0,
                    "run_number": 1,
                    "winner": "A",
                    "reasoning": "A is better.",
                    "rubric": {
                        "A": {"content_score": 9, "structure_score": 9, "overall_score": 9},
                        "B": {"content_score": 5, "structure_score": 5, "overall_score": 5},
                    },
                    "expectation_results": {
                        "A": {"passed": 2, "total": 2, "pass_rate": 1.0},
                        "B": {"passed": 1, "total": 2, "pass_rate": 0.5},
                    },
                }
            ],
        }
        self._write_json(self.iteration_dir / "_meta" / "raw-comparison-create-element-eval-0-run-1.json", duplicate_payload)
        self._write_json(self.iteration_dir / "_meta" / "create-element-blind.json", duplicate_payload)

        summary = tools.collect_harness_noise(self.iteration_dir, self.workspace_root)

        self.assertEqual(summary["status"], "observed")
        self.assertEqual(summary["event_count"], 2)
        categories = {event["category"] for event in summary["events"]}
        self.assertEqual(categories, {"denied-broad-discovery", "duplicate-raw-comparison-payload"})
        self.assertTrue((self.iteration_dir / "_meta" / "harness-noise.json").exists())

    def test_build_synthesis_bundle_returns_quantitative_and_per_eval(self) -> None:
        skill_dir = self.iteration_dir / "create-element"
        with_response = skill_dir / "eval-0" / "with_skill" / "response.md"
        without_response = skill_dir / "eval-0" / "without_skill" / "response.md"
        with_response.parent.mkdir(parents=True, exist_ok=True)
        without_response.parent.mkdir(parents=True, exist_ok=True)
        with_response.write_text("with skill answer\n", encoding="utf-8")
        without_response.write_text("without skill answer\n", encoding="utf-8")

        self._write_json(
            skill_dir / "with_skill-run-metrics.json",
            {
                "skill_name": "create-element",
                "configuration": "with_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:00:00Z",
                "finished_at": "2026-03-13T10:00:05Z",
                "elapsed_seconds_total": 5.0,
                "files_read_count": 1,
                "files_written_count": 1,
            },
        )
        self._write_json(
            skill_dir / "without_skill-run-metrics.json",
            {
                "skill_name": "create-element",
                "configuration": "without_skill",
                "language": "English",
                "mcp_used": False,
                "started_at": "2026-03-13T10:01:00Z",
                "finished_at": "2026-03-13T10:01:08Z",
                "elapsed_seconds_total": 8.0,
                "files_read_count": 0,
                "files_written_count": 1,
            },
        )

        self._write_json(skill_dir / "eval-0" / "blind-map.run-1.json", {"A": "with_skill", "B": "without_skill"})
        self._write_json(
            skill_dir / "blind-comparisons.json",
            {
                "schema_version": 2,
                "skill_name": "create-element",
                "comparisons": [
                    {
                        "schema_version": 2,
                        "eval_id": 0,
                        "run_number": 1,
                        "winner": "A",
                        "reasoning": "A provides the correct Container_Api kind.",
                        "rubric": {
                            "A": {"content_score": 9, "structure_score": 9, "overall_score": 9, "notes": "Correct kind"},
                            "B": {"content_score": 5, "structure_score": 5, "overall_score": 5, "notes": "Wrong kind"},
                        },
                        "expectation_results": {
                            "A": {"passed": 2, "total": 2, "pass_rate": 1.0},
                            "B": {"passed": 1, "total": 2, "pass_rate": 0.5},
                        },
                    }
                ],
            },
        )

        # Build config summaries needed by the bundle
        evals_path = self.workspace_root / ".github" / "skills" / "create-element" / "evals" / "evals-public.json"
        tools.summarize_config(skill_dir, "with_skill", evals_path)
        tools.summarize_config(skill_dir, "without_skill", evals_path)

        bundle = tools.build_synthesis_bundle(self.iteration_dir, self.workspace_root, "create-element")

        # Structural checks
        self.assertEqual(bundle["skill_name"], "create-element")
        self.assertEqual(bundle["eval_count"], 1)
        self.assertIn("quantitative", bundle)
        self.assertIn("per_eval_comparisons", bundle)
        self.assertIn("synthesis_template", bundle)

        # Quantitative checks
        q = bundle["quantitative"]
        self.assertEqual(q["blind"]["with_skill_wins"], 1)
        self.assertEqual(q["blind"]["with_skill_win_rate"], 1.0)
        self.assertEqual(q["expectation_pass_rate"]["with_skill"], 1.0)
        self.assertEqual(q["expectation_pass_rate"]["without_skill"], 0.5)
        self.assertEqual(q["rubric_score"]["with_skill"], 9.0)
        self.assertEqual(q["rubric_score"]["without_skill"], 5.0)

        # Per-eval comparison checks
        self.assertEqual(len(bundle["per_eval_comparisons"]), 1)
        comp = bundle["per_eval_comparisons"][0]
        self.assertEqual(comp["eval_id"], 0)
        self.assertEqual(comp["winner"], "with_skill")
        self.assertEqual(comp["confidence"], "high")
        self.assertIn("Container_Api", comp["reasoning"])
        self.assertEqual(comp["eval_prompt"], "Add an API container.")
        self.assertEqual(comp["with_skill_expectations"]["passed"], 2)
        self.assertEqual(comp["without_skill_expectations"]["passed"], 1)
        self.assertEqual(comp["with_skill_rubric_notes"], "Correct kind")

    def test_write_synthesis_saves_content(self) -> None:
        skill_dir = self.iteration_dir / "create-element"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = "# Test Synthesis\nSome content here."
        content_file = self.workspace_root / "tmp-synthesis.md"
        content_file.write_text(content, encoding="utf-8")

        import argparse
        args = argparse.Namespace(
            iteration=self.iteration_dir,
            workspace_root=self.workspace_root,
            skill="create-element",
            content_file=content_file,
            output=None,
        )
        tools.cmd_write_synthesis(args)

        output_path = skill_dir / "synthesis.md"
        self.assertTrue(output_path.exists())
        self.assertEqual(output_path.read_text(encoding="utf-8"), content)


if __name__ == "__main__":
    unittest.main()
