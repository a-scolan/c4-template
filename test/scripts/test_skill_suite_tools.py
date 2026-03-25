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

        self._write_json(skill_dir / "eval-0" / "blind-map.json", {"A": "with_skill", "B": "without_skill"})
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
        (self.workspace_root / "test" / "_agent-hooks").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "test" / "_live-mcp-probe").mkdir(parents=True, exist_ok=True)
        (self.workspace_root / "test" / "scripts" / "__pycache__").mkdir(parents=True, exist_ok=True)

        summary = tools.clean_benchmark_artifacts(self.workspace_root)

        self.assertEqual(summary["removed_count"], 6)
        self.assertFalse((self.workspace_root / "test" / "iteration-1").exists())
        self.assertFalse((self.workspace_root / "test" / "iteration-2").exists())
        self.assertFalse((self.workspace_root / "test" / "iteration-9").exists())
        self.assertFalse((self.workspace_root / "test" / "_agent-hooks").exists())
        self.assertFalse((self.workspace_root / "test" / "_live-mcp-probe").exists())
        self.assertFalse((self.workspace_root / "test" / "scripts" / "__pycache__").exists())
        self.assertTrue((self.workspace_root / "test" / "_meta" / "clean-benchmark-artifacts.json").exists())

    def test_snapshot_public_evals_writes_iteration_meta_copy(self) -> None:
        summary = tools.snapshot_public_evals(self.iteration_dir, self.workspace_root)

        self.assertEqual(summary["skill_count"], 1)
        self.assertEqual(summary["skills"][0]["skill_name"], "create-element")
        self.assertEqual(summary["skills"][0]["evals"][0]["prompt"], "Add an API container.")
        snapshot_path = self.iteration_dir / "_meta" / "evals-public-snapshot.json"
        self.assertTrue(snapshot_path.exists())

    def test_current_utc_timestamp_returns_iso8601_utc_string(self) -> None:
        payload = tools.current_utc_timestamp()

        self.assertIn("timestamp", payload)
        self.assertIsNotNone(tools.iso_to_datetime(payload["timestamp"]))
        self.assertTrue(payload["timestamp"].endswith("Z"))

    def test_validate_hook_audit_accepts_denied_broad_mcp_and_shared_reads(self) -> None:
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
                            "tool_paths": ["projects/shared/spec-context.c4"],
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


if __name__ == "__main__":
    unittest.main()
