from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
HOOK_SCRIPT = ROOT / "test" / "scripts" / "benchmark_access_hook.py"
ALLOWED_SUBAGENTS = "Skill Benchmark Baseline,Skill Benchmark Baseline Hook-Only,Skill Benchmark With Skill,Skill Blind Comparator"


class BenchmarkAgentPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace_dir = tempfile.TemporaryDirectory()
        self.workspace_root = Path(self.workspace_dir.name).resolve()
        self.state_root = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace_dir.cleanup)
        self.addCleanup(self.state_root.cleanup)
        self.create_workspace_fixture()

    def create_workspace_fixture(self) -> None:
        (self.workspace_root / "README.md").write_text("# temp workspace\n", encoding="utf-8")
        blind_dir_old = self.workspace_root / "test" / "iteration-1" / "create-element" / "eval-0" / "blind"
        blind_dir_old.mkdir(parents=True, exist_ok=True)
        (blind_dir_old / "A.md").write_text("blind artifact old\n", encoding="utf-8")
        (blind_dir_old.parent / "blind-map.json").write_text("{}\n", encoding="utf-8")
        blind_dir = self.workspace_root / "test" / "iteration-2" / "create-element" / "eval-0" / "blind"
        blind_dir.mkdir(parents=True, exist_ok=True)
        (blind_dir / "A.md").write_text("blind artifact current\n", encoding="utf-8")
        (blind_dir.parent / "blind-map.json").write_text("{}\n", encoding="utf-8")
        (blind_dir.parent.parent / "blind-comparisons.json").write_text("{}\n", encoding="utf-8")
        skill_series_blind_dir = self.workspace_root / "test" / "likec4-dsl-test4" / "likec4-dsl" / "eval-0" / "blind"
        skill_series_blind_dir.mkdir(parents=True, exist_ok=True)
        (skill_series_blind_dir / "A.md").write_text("blind artifact series A\n", encoding="utf-8")
        (skill_series_blind_dir / "B.md").write_text("blind artifact series B\n", encoding="utf-8")
        (skill_series_blind_dir.parent / "blind-map.json").write_text("{}\n", encoding="utf-8")
        (skill_series_blind_dir.parent.parent / "blind-comparisons.json").write_text("{}\n", encoding="utf-8")
        run_blind_dir = skill_series_blind_dir / "run-1"
        run_blind_dir.mkdir(parents=True, exist_ok=True)
        (run_blind_dir / "A.md").write_text("blind artifact series run A\n", encoding="utf-8")
        (run_blind_dir / "B.md").write_text("blind artifact series run B\n", encoding="utf-8")
        disabled_skill = self.workspace_root / "test" / "iteration-1" / "_disabled-skills" / "create-element"
        disabled_skill.mkdir(parents=True, exist_ok=True)
        (disabled_skill / "SKILL.md").write_text("# disabled create-element\n", encoding="utf-8")
        shared_root = self.workspace_root / "projects" / "shared"
        shared_root.mkdir(parents=True, exist_ok=True)
        (shared_root / "spec-context.c4").write_text("specification example\n", encoding="utf-8")
        template_root = self.workspace_root / "projects" / "template"
        template_root.mkdir(parents=True, exist_ok=True)
        (template_root / "system-model.c4").write_text("template example\n", encoding="utf-8")
        (self.workspace_root / ".github" / "agents").mkdir(parents=True, exist_ok=True)

        create_element_root = self.workspace_root / ".github" / "skills" / "create-element"
        (create_element_root / "evals").mkdir(parents=True, exist_ok=True)
        (create_element_root / "SKILL.md").write_text("# create-element\n", encoding="utf-8")
        (create_element_root / "evals" / "evals-public.json").write_text("{}\n", encoding="utf-8")
        (create_element_root / "evals" / "grading-spec.json").write_text("{}\n", encoding="utf-8")

        create_relationship_root = self.workspace_root / ".github" / "skills" / "create-relationship"
        create_relationship_root.mkdir(parents=True, exist_ok=True)
        (create_relationship_root / "SKILL.md").write_text("# create-relationship\n", encoding="utf-8")

        skill_creator_agents = self.workspace_root / ".github" / "skills" / "skill-creator" / "agents"
        skill_creator_agents.mkdir(parents=True, exist_ok=True)
        (skill_creator_agents / "comparator.md").write_text("# comparator\n", encoding="utf-8")

        likec4_dsl_root = self.workspace_root / ".github" / "skills" / "likec4-dsl"
        (likec4_dsl_root / "evals").mkdir(parents=True, exist_ok=True)
        (likec4_dsl_root / "SKILL.md").write_text("# likec4-dsl\n", encoding="utf-8")
        (likec4_dsl_root / "evals" / "grading-spec.json").write_text("{}\n", encoding="utf-8")

    def clear_workspace_skills(self) -> None:
        skills_root = self.workspace_root / ".github" / "skills"
        if not skills_root.exists():
            return
        for child in list(skills_root.iterdir()):
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

    def payload(
        self,
        *,
        session_id: Any | None,
        tool_name: str,
        tool_input: dict[str, Any],
        timestamp: str = "2026-03-12T12:00:00Z",
        include_hook_event_name: bool = True,
    ) -> dict[str, Any]:
        payload = {
            "timestamp": timestamp,
            "cwd": self.workspace_root.as_posix(),
            "sessionId": session_id,
            "tool_name": tool_name,
            "tool_input": tool_input,
        }
        if include_hook_event_name:
            payload["hookEventName"] = "PreToolUse"
        return payload

    def read_payload(
        self,
        session_id: Any | None,
        relative_path: str,
        *,
        start_line: int = 1,
        end_line: int = 50,
        timestamp: str = "2026-03-12T12:00:00Z",
    ) -> dict[str, Any]:
        return self.payload(
            session_id=session_id,
            tool_name="read_file",
            tool_input={
                "filePath": (self.workspace_root / relative_path).as_posix(),
                "startLine": start_line,
                "endLine": end_line,
            },
            timestamp=timestamp,
        )

    def session_start_payload(self, session_id: Any | None, timestamp: str = "2026-03-12T12:00:00Z") -> dict[str, Any]:
        return {
            "timestamp": timestamp,
            "cwd": self.workspace_root.as_posix(),
            "sessionId": session_id,
            "hookEventName": "SessionStart",
        }

    def subagent_payload(self, session_id: str, agent_name: str, description: str, prompt: str) -> dict[str, Any]:
        return self.payload(
            session_id=session_id,
            tool_name="runSubagent",
            tool_input={
                "agentName": agent_name,
                "description": description,
                "prompt": prompt,
            },
        )

    def command_payload(self, session_id: str, command: str) -> dict[str, Any]:
        return self.payload(
            session_id=session_id,
            tool_name="run_in_terminal",
            tool_input={
                "command": command,
                "goal": "shell escape",
                "explanation": "unsafe command",
                "isBackground": False,
                "timeout": 0,
            },
        )

    def create_file_payload(self, session_id: str, relative_path: str, content: str) -> dict[str, Any]:
        return self.payload(
            session_id=session_id,
            tool_name="create_file",
            tool_input={
                "filePath": (self.workspace_root / relative_path).as_posix(),
                "content": content,
            },
        )

    def mcp_payload(
        self,
        session_id: str,
        tool_name: str,
        tool_input: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.payload(
            session_id=session_id,
            tool_name=tool_name,
            tool_input=tool_input or {},
        )

    def run_hook_payload(self, payload: dict[str, Any], *, mode: str, extra_env: dict[str, str] | None = None) -> dict[str, Any]:
        env = os.environ.copy()
        env.update(
            {
                "BENCH_MODE": mode,
                "BENCH_STATE_ROOT": self.state_root.name,
            }
        )
        if extra_env:
            env.update(extra_env)
        result = subprocess.run(
            [sys.executable, str(HOOK_SCRIPT)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
            cwd=self.workspace_root,
            env=env,
        )
        if result.returncode != 0:
            self.fail(f"hook exited with {result.returncode}: {result.stderr}\nstdout={result.stdout}")
        return json.loads(result.stdout)

    def read_jsonl(self, relative_path: str) -> list[dict[str, Any]]:
        path = self.workspace_root / relative_path
        if not path.exists():
            return []
        records: list[dict[str, Any]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
        return records

    def decision(self, output: dict[str, Any]) -> str:
        return output["hookSpecificOutput"]["permissionDecision"]

    def test_baseline_allows_shared_specs_after_relocation(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.read_payload("baseline-session", "projects/shared/spec-context.c4", end_line=20),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_baseline_denies_readme_after_relocation(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(self.read_payload("baseline-session", "README.md", end_line=20), mode="baseline")
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_denies_readme_when_live_payload_omits_hook_event_name(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.payload(
                session_id="baseline-live-session",
                tool_name="read_file",
                tool_input={
                    "filePath": (self.workspace_root / "README.md").as_posix(),
                    "startLine": 1,
                    "endLine": 20,
                },
                include_hook_event_name=False,
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_denies_when_skills_are_still_present(self) -> None:
        output = self.run_hook_payload(self.read_payload("baseline-session", "README.md", end_line=20), mode="baseline")
        self.assertEqual(self.decision(output), "deny")
        self.assertIn("relocating workspace skills", output["hookSpecificOutput"]["permissionDecisionReason"])

    def test_baseline_hook_only_allows_shared_specs_without_relocation(self) -> None:
        output = self.run_hook_payload(
            self.read_payload("baseline-session", "projects/shared/spec-context.c4", end_line=20),
            mode="baseline_hook_only",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_baseline_hook_only_denies_readme(self) -> None:
        output = self.run_hook_payload(
            self.read_payload("baseline-session", "README.md", end_line=20),
            mode="baseline_hook_only",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_hook_only_denies_skill_reads(self) -> None:
        output = self.run_hook_payload(
            self.read_payload("baseline-session", ".github/skills/create-element/SKILL.md", end_line=50),
            mode="baseline_hook_only",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_denies_test_artifacts(self) -> None:
        output = self.run_hook_payload(
            self.read_payload("baseline-session", "test/iteration-2/create-element/eval-0/blind/A.md", end_line=20),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_denies_disabled_skill_backup(self) -> None:
        output = self.run_hook_payload(
            self.read_payload("baseline-session", "test/iteration-1/_disabled-skills/create-element/SKILL.md", end_line=20),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_denies_nonshared_project_examples(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.read_payload("baseline-session", "projects/template/system-model.c4", end_line=20),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_manager_allows_only_allowlisted_subagents(self) -> None:
        output = self.run_hook_payload(
            self.subagent_payload(
                "manager-session",
                "Skill Benchmark Baseline",
                "run baseline worker",
                "Execute the without_skill phase for create-element.",
            ),
            mode="benchmark_manager",
            extra_env={"BENCH_ALLOWED_AGENTS": ALLOWED_SUBAGENTS},
        )
        self.assertEqual(self.decision(output), "allow")

    def test_manager_denies_unconstrained_subagents(self) -> None:
        output = self.run_hook_payload(
            self.subagent_payload(
                "manager-session",
                "Explore",
                "unsafe exploratory worker",
                "Search the repo for anything useful.",
            ),
            mode="benchmark_manager",
            extra_env={"BENCH_ALLOWED_AGENTS": ALLOWED_SUBAGENTS},
        )
        self.assertEqual(self.decision(output), "deny")

    def test_manager_denies_mcp_tools(self) -> None:
        output = self.run_hook_payload(
            self.payload(
                session_id="manager-session-mcp",
                tool_name="mcp_context7_query-docs",
                tool_input={
                    "libraryId": "/likec4/likec4",
                    "query": "How do custom agents restrict tools?",
                },
            ),
            mode="benchmark_manager",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_manager_denies_likec4_mcp_tools(self) -> None:
        output = self.run_hook_payload(
            self.mcp_payload(
                "manager-session-likec4",
                "mcp_likec4_read-project-summary",
                {"project": "template"},
            ),
            mode="benchmark_manager",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_denies_broad_likec4_project_browsing_after_relocation(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.mcp_payload(
                "baseline-mcp-session",
                "mcp_likec4_read-project-summary",
                {"project": "template"},
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_allows_narrow_likec4_grounding_after_relocation(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.mcp_payload(
                "baseline-mcp-extra-session",
                "mcp_likec4_search-element",
                {"search": "Container_Api"},
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_baseline_resolved_audit_records_denied_broad_likec4_browsing(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.mcp_payload(
                "baseline-audit-deny-session",
                "mcp_likec4_read-project-summary",
                {"project": "template"},
            ),
            mode="baseline",
            extra_env={
                "BENCH_DEBUG_HOOKS": "1",
                "BENCH_DEBUG_LOG": "test/_agent-hooks/hook-debug.jsonl",
            },
        )
        self.assertEqual(self.decision(output), "deny")

        audit_records = self.read_jsonl("test/_agent-hooks/hook-audit.jsonl")
        self.assertTrue(audit_records)
        self.assertEqual(audit_records[-1]["tool_name"], "mcp_likec4_read-project-summary")
        self.assertEqual(audit_records[-1]["permissionDecision"], "deny")

    def test_baseline_resolved_audit_records_allowed_shared_read(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.read_payload("baseline-audit-allow-session", "projects/shared/spec-context.c4", end_line=20),
            mode="baseline",
            extra_env={
                "BENCH_DEBUG_HOOKS": "1",
                "BENCH_DEBUG_LOG": "test/_agent-hooks/hook-debug.jsonl",
            },
        )
        self.assertEqual(self.decision(output), "allow")

        audit_records = self.read_jsonl("test/_agent-hooks/hook-audit.jsonl")
        self.assertTrue(audit_records)
        self.assertEqual(audit_records[-1]["tool_name"], "read_file")
        self.assertEqual(audit_records[-1]["permissionDecision"], "allow")
        self.assertEqual(audit_records[-1]["tool_paths"], ["projects/shared/spec-context.c4"])

    def test_baseline_denies_non_likec4_mcp_tools(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.mcp_payload(
                "baseline-context7-session",
                "mcp_context7_query-docs",
                {"libraryId": "/likec4/likec4", "query": "views"},
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_hook_only_denies_broad_likec4_project_browsing(self) -> None:
        output = self.run_hook_payload(
            self.mcp_payload(
                "baseline-hook-mcp-session",
                "mcp_likec4_list-projects",
            ),
            mode="baseline_hook_only",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_hook_only_allows_narrow_likec4_grounding(self) -> None:
        output = self.run_hook_payload(
            self.mcp_payload(
                "baseline-hook-mcp-search-session",
                "mcp_likec4_search-element",
                {"search": "Container_Api"},
            ),
            mode="baseline_hook_only",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_with_skill_allows_narrow_likec4_grounding(self) -> None:
        output = self.run_hook_payload(
            self.mcp_payload(
                "with-skill-mcp-session",
                "mcp_likec4_search-element",
                {"search": "corePlatform"},
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_with_skill_denies_broad_likec4_project_browsing(self) -> None:
        output = self.run_hook_payload(
            self.mcp_payload(
                "with-skill-project-session",
                "mcp_likec4_read-project-summary",
                {"project": "template"},
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_with_skill_denies_non_likec4_mcp_tools(self) -> None:
        output = self.run_hook_payload(
            self.mcp_payload(
                "with-skill-context7-session",
                "mcp_context7_query-docs",
                {"libraryId": "/likec4/likec4", "query": "views"},
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_blind_comparator_denies_likec4_mcp_tools(self) -> None:
        output = self.run_hook_payload(
            self.mcp_payload(
                "blind-likec4-session",
                "mcp_likec4_read-project-summary",
                {"project": "template"},
            ),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_with_skill_locks_first_skill_directory(self) -> None:
        first = self.run_hook_payload(
            self.read_payload("with-skill-session", ".github/skills/create-element/SKILL.md", end_line=80),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(first), "allow")

        second = self.run_hook_payload(
            self.read_payload(
                "with-skill-session",
                ".github/skills/create-relationship/SKILL.md",
                end_line=80,
                timestamp="2026-03-12T12:00:10Z",
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(second), "deny")

    def test_with_skill_session_start_resets_stale_skill_lock(self) -> None:
        first = self.run_hook_payload(
            self.read_payload("with-skill-reset-session", ".github/skills/create-element/SKILL.md", end_line=80),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(first), "allow")

        denied = self.run_hook_payload(
            self.read_payload(
                "with-skill-reset-session",
                ".github/skills/create-relationship/SKILL.md",
                end_line=80,
                timestamp="2026-03-12T12:00:10Z",
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(denied), "deny")

        self.run_hook_payload(
            self.session_start_payload("with-skill-reset-session", timestamp="2026-03-12T12:00:20Z"),
            mode="with_skill_targeted",
        )

        allowed_after_reset = self.run_hook_payload(
            self.read_payload(
                "with-skill-reset-session",
                ".github/skills/create-relationship/SKILL.md",
                end_line=80,
                timestamp="2026-03-12T12:00:30Z",
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(allowed_after_reset), "allow")

    def test_with_skill_missing_session_id_uses_skill_scoped_anonymous_state_file(self) -> None:
        output = self.run_hook_payload(
            self.read_payload(None, ".github/skills/create-element/SKILL.md", end_line=80),
            mode="with_skill_targeted",
        )

        self.assertEqual(self.decision(output), "allow")
        anonymous_state_path = Path(self.state_root.name) / "anonymous-with_skill_targeted-create-element.json"
        self.assertTrue(anonymous_state_path.exists())
        self.assertFalse((Path(self.state_root.name) / "default.json").exists())

        stored_state = json.loads(anonymous_state_path.read_text(encoding="utf-8"))
        self.assertEqual(stored_state.get("session_id"), "anonymous-with_skill_targeted-create-element")
        self.assertEqual(stored_state.get("locked_skill"), "create-element")

    def test_with_skill_missing_session_id_derives_distinct_sessions_per_skill_for_parallel_workers(self) -> None:
        create_element = self.run_hook_payload(
            self.read_payload(None, ".github/skills/create-element/SKILL.md", end_line=80),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(create_element), "allow")

        create_relationship = self.run_hook_payload(
            self.read_payload(
                None,
                ".github/skills/create-relationship/SKILL.md",
                end_line=80,
                timestamp="2026-03-12T12:00:10Z",
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(create_relationship), "allow")

        state_root = Path(self.state_root.name)
        self.assertTrue((state_root / "anonymous-with_skill_targeted-create-element.json").exists())
        self.assertTrue((state_root / "anonymous-with_skill_targeted-create-relationship.json").exists())

    def test_blind_compare_missing_session_id_uses_iteration_scoped_anonymous_state(self) -> None:
        first = self.run_hook_payload(
            self.read_payload(None, "test/iteration-1/create-element/eval-0/blind/A.md", end_line=40),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(first), "allow")

        second = self.run_hook_payload(
            self.read_payload(
                None,
                "test/iteration-2/create-element/eval-0/blind/A.md",
                end_line=40,
                timestamp="2026-03-12T12:00:10Z",
            ),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(second), "allow")

        state_root = Path(self.state_root.name)
        self.assertTrue((state_root / "anonymous-blind_compare-iteration-1-create-element.json").exists())
        self.assertTrue((state_root / "anonymous-blind_compare-iteration-2-create-element.json").exists())

    def test_blind_compare_allows_skill_series_blind_artifacts(self) -> None:
        blind = self.run_hook_payload(
            self.read_payload(None, "test/likec4-dsl-test4/likec4-dsl/eval-0/blind/A.md", end_line=40),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(blind), "allow")

        blind_run = self.run_hook_payload(
            self.read_payload(
                None,
                "test/likec4-dsl-test4/likec4-dsl/eval-0/blind/run-1/B.md",
                end_line=40,
                timestamp="2026-03-12T12:00:10Z",
            ),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(blind_run), "allow")

    def test_blind_compare_allows_scoped_search_within_blind_directory(self) -> None:
        output = self.run_hook_payload(
            self.payload(
                session_id=None,
                tool_name="grep_search",
                tool_input={
                    "query": "blind artifact",
                    "isRegexp": False,
                    "includePattern": "test/likec4-dsl-test4/likec4-dsl/eval-0/blind/run-1/**",
                },
            ),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_blind_compare_denies_search_outside_blind_scope(self) -> None:
        output = self.run_hook_payload(
            self.payload(
                session_id=None,
                tool_name="grep_search",
                tool_input={
                    "query": "benchmark",
                    "isRegexp": False,
                    "includePattern": "test/likec4-dsl-test4/likec4-dsl/**",
                },
            ),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_blind_compare_missing_session_id_uses_skill_series_scoped_anonymous_state(self) -> None:
        output = self.run_hook_payload(
            self.read_payload(None, "test/likec4-dsl-test4/likec4-dsl/eval-0/blind/A.md", end_line=40),
            mode="blind_compare",
        )

        self.assertEqual(self.decision(output), "allow")
        state_root = Path(self.state_root.name)
        self.assertTrue((state_root / "anonymous-blind_compare-likec4-dsl-test4-likec4-dsl.json").exists())

        grading = self.run_hook_payload(
            self.read_payload(
                None,
                ".github/skills/likec4-dsl/evals/grading-spec.json",
                end_line=40,
                timestamp="2026-03-12T12:00:10Z",
            ),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(grading), "allow")

    def test_with_skill_anonymous_session_start_resets_scoped_state_and_warns_about_serial_execution(self) -> None:
        first = self.run_hook_payload(
            self.read_payload(None, ".github/skills/create-element/SKILL.md", end_line=80),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(first), "allow")

        second = self.run_hook_payload(
            self.read_payload(
                None,
                ".github/skills/create-relationship/SKILL.md",
                end_line=80,
                timestamp="2026-03-12T12:00:10Z",
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(second), "allow")

        session_start = self.run_hook_payload(
            self.session_start_payload(None, timestamp="2026-03-12T12:00:20Z"),
            mode="with_skill_targeted",
        )
        additional_context = session_start["hookSpecificOutput"]["additionalContext"]
        self.assertIn("serially", additional_context)
        self.assertIn("anonymous-with_skill_targeted", additional_context)

        allowed_after_reset = self.run_hook_payload(
            self.read_payload(
                None,
                ".github/skills/create-relationship/SKILL.md",
                end_line=80,
                timestamp="2026-03-12T12:00:30Z",
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(allowed_after_reset), "allow")

    def test_with_skill_allows_shared_specs_but_denies_nonshared_projects(self) -> None:
        shared = self.run_hook_payload(
            self.read_payload("with-skill-shared-session", "projects/shared/spec-context.c4", end_line=40),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(shared), "allow")

        denied = self.run_hook_payload(
            self.read_payload(
                "with-skill-shared-session",
                "projects/template/system-model.c4",
                end_line=40,
                timestamp="2026-03-12T12:00:10Z",
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(denied), "deny")

    def test_with_skill_denies_test_artifacts_even_for_locked_skill(self) -> None:
        first = self.run_hook_payload(
            self.read_payload("with-skill-test-session", ".github/skills/create-element/SKILL.md", end_line=80),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(first), "allow")

        denied = self.run_hook_payload(
            self.read_payload(
                "with-skill-test-session",
                "test/iteration-2/create-element/eval-0/blind/A.md",
                end_line=40,
                timestamp="2026-03-12T12:00:10Z",
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(denied), "deny")

    def test_with_skill_allows_public_evals_but_denies_hidden_grading(self) -> None:
        public_evals = self.run_hook_payload(
            self.read_payload("with-skill-evals-session", ".github/skills/create-element/evals/evals-public.json", end_line=80),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(public_evals), "allow")

        hidden_grading = self.run_hook_payload(
            self.read_payload(
                "with-skill-evals-session",
                ".github/skills/create-element/evals/grading-spec.json",
                end_line=80,
                timestamp="2026-03-12T12:00:10Z",
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(hidden_grading), "deny")

    def test_blind_comparator_denies_mapping_file(self) -> None:
        output = self.run_hook_payload(
            self.read_payload("blind-session", "test/iteration-2/create-element/eval-0/blind-map.json", end_line=40),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_blind_comparator_allows_blind_artifacts_and_grading_spec(self) -> None:
        blind = self.run_hook_payload(
            self.read_payload("blind-session-2", "test/iteration-2/create-element/eval-0/blind/A.md", end_line=120),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(blind), "allow")

        grading = self.run_hook_payload(
            self.read_payload(
                "blind-session-2",
                ".github/skills/create-element/evals/grading-spec.json",
                end_line=200,
                timestamp="2026-03-12T12:00:10Z",
            ),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(grading), "allow")

    def test_blind_comparator_denies_public_eval_artifacts(self) -> None:
        output = self.run_hook_payload(
            self.read_payload("blind-public-session", ".github/skills/create-element/evals/evals-public.json", end_line=40),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_blind_comparator_locks_first_iteration_read_instead_of_assuming_latest(self) -> None:
        first = self.run_hook_payload(
            self.read_payload("blind-old-session", "test/iteration-1/create-element/eval-0/blind/A.md", end_line=40),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(first), "allow")

        second = self.run_hook_payload(
            self.read_payload(
                "blind-old-session",
                "test/iteration-2/create-element/eval-0/blind/A.md",
                end_line=40,
                timestamp="2026-03-12T12:00:10Z",
            ),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(second), "deny")

    def test_blind_comparator_denies_previous_comparison_results(self) -> None:
        output = self.run_hook_payload(
            self.read_payload("blind-results-session", "test/iteration-2/create-element/blind-comparisons.json", end_line=40),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_manager_command_allowlist_blocks_shell_escape(self) -> None:
        output = self.run_hook_payload(
            self.command_payload("manager-session-2", "python -c \"print('hello from outside the allowlist')\""),
            mode="benchmark_manager",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_manager_denies_sensitive_skill_suite_command_without_iteration(self) -> None:
        output = self.run_hook_payload(
            self.command_payload(
                "manager-session-no-iteration",
                "python test/scripts/skill_suite_tools.py aggregate --workspace-root .",
            ),
            mode="benchmark_manager",
        )
        self.assertEqual(self.decision(output), "deny")
        self.assertIn("must provide an explicit --iteration", output["hookSpecificOutput"]["permissionDecisionReason"])

    def test_manager_allows_pre_aggregate_check_with_iteration(self) -> None:
        output = self.run_hook_payload(
            self.command_payload(
                "manager-session-precheck",
                "python test/scripts/skill_suite_tools.py pre-aggregate-check --iteration test/iteration-2 --workspace-root .",
            ),
            mode="benchmark_manager",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_manager_allows_resume_finalize_with_iteration(self) -> None:
        output = self.run_hook_payload(
            self.command_payload(
                "manager-session-resume-finalize",
                "python test/scripts/skill_suite_tools.py resume-finalize --iteration test/iteration-2 --workspace-root .",
            ),
            mode="benchmark_manager",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_manager_locks_iteration_across_sensitive_commands(self) -> None:
        first = self.run_hook_payload(
            self.command_payload(
                "manager-session-iteration-lock",
                "python test/scripts/skill_suite_tools.py aggregate --iteration test/likec4-dsl-test2 --workspace-root .",
            ),
            mode="benchmark_manager",
        )
        self.assertEqual(self.decision(first), "allow")

        second = self.run_hook_payload(
            self.command_payload(
                "manager-session-iteration-lock",
                "python test/scripts/skill_suite_tools.py aggregate --iteration test/iteration-2 --workspace-root .",
            ),
            mode="benchmark_manager",
        )
        self.assertEqual(self.decision(second), "deny")
        self.assertIn("Iteration scope is locked", second["hookSpecificOutput"]["permissionDecisionReason"])

    def test_manager_create_file_allows_json_content_with_path_like_strings(self) -> None:
        output = self.run_hook_payload(
            self.create_file_payload(
                "manager-create-file-session",
                "test/iteration-2/_meta/example.json",
                '{"output_path":"test/iteration-2/create-element/blind-comparisons.json","note":"C:/temp/report.md"}',
            ),
            mode="benchmark_manager",
        )
        self.assertEqual(self.decision(output), "allow")

    # --- Worker write access tests ---

    def test_baseline_worker_allows_write_under_iteration_skill(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.create_file_payload(
                "baseline-write-session",
                "test/iteration-2/create-element/eval-0/without_skill/run-1/response.md",
                "# Benchmark response\n",
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_baseline_worker_denies_write_under_scripts(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.create_file_payload(
                "baseline-write-scripts-session",
                "test/scripts/malicious.py",
                "import os; os.system('evil')\n",
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_worker_denies_write_under_agent_hooks(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.create_file_payload(
                "baseline-write-hooks-session",
                "test/_agent-hooks/injected.json",
                "{}",
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_worker_denies_write_under_meta(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.create_file_payload(
                "baseline-write-meta-session",
                "test/_meta/injected.json",
                "{}",
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_worker_denies_write_outside_test(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.create_file_payload(
                "baseline-write-outside-session",
                "projects/shared/injected.c4",
                "specification {}",
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_baseline_worker_denies_write_to_disabled_skills(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.create_file_payload(
                "baseline-write-disabled-session",
                "test/iteration-2/_disabled-skills/create-element/SKILL.md",
                "# injected\n",
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_with_skill_worker_allows_write_under_iteration_skill(self) -> None:
        output = self.run_hook_payload(
            self.create_file_payload(
                "with-skill-write-session",
                "test/iteration-2/create-element/eval-0/with_skill/run-1/response.md",
                "# Skill-assisted response\n",
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_with_skill_worker_denies_write_to_non_iteration_dir(self) -> None:
        output = self.run_hook_payload(
            self.create_file_payload(
                "with-skill-write-noniter-session",
                "test/random-folder/response.md",
                "# Response\n",
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_worker_write_lock_denies_switching_iteration_in_same_session(self) -> None:
        self.clear_workspace_skills()
        first = self.run_hook_payload(
            self.create_file_payload(
                "baseline-write-lock-session",
                "test/likec4-dsl-test4/create-element/eval-0/without_skill/run-1/response.md",
                "# First response\n",
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(first), "allow")

        second = self.run_hook_payload(
            self.create_file_payload(
                "baseline-write-lock-session",
                "test/iteration-2/create-element/eval-0/without_skill/run-1/response.md",
                "# Second response\n",
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(second), "deny")
        self.assertIn("Iteration scope is locked", second["hookSpecificOutput"]["permissionDecisionReason"])

    def test_baseline_worker_allows_write_to_skill_series_iteration(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.create_file_payload(
                "baseline-write-series-session",
                "test/likec4-dsl-test4/likec4-dsl/eval-0/without_skill/run-1/response.md",
                "# Series iteration response\n",
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_blind_compare_denies_write(self) -> None:
        output = self.run_hook_payload(
            self.create_file_payload(
                "blind-write-session",
                "test/iteration-2/create-element/eval-0/blind/result.json",
                "{}",
            ),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(output), "deny")

    def test_with_skill_worker_allows_replace_string_in_file_under_iteration(self) -> None:
        output = self.run_hook_payload(
            self.payload(
                session_id="with-skill-replace-session",
                tool_name="replace_string_in_file",
                tool_input={
                    "filePath": (self.workspace_root / "test/iteration-2/create-element/eval-0/with_skill/run-1/response.md").as_posix(),
                    "oldString": "old content",
                    "newString": "new content",
                },
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_with_skill_worker_allows_multi_replace_under_iteration(self) -> None:
        output = self.run_hook_payload(
            self.payload(
                session_id="with-skill-multi-replace-session",
                tool_name="multi_replace_string_in_file",
                tool_input={
                    "replacements": [
                        {
                            "filePath": (self.workspace_root / "test/iteration-2/create-element/eval-0/with_skill/run-1/response.md").as_posix(),
                            "oldString": "old",
                            "newString": "new",
                        },
                    ],
                },
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_with_skill_worker_denies_replace_outside_iteration(self) -> None:
        output = self.run_hook_payload(
            self.payload(
                session_id="with-skill-replace-outside-session",
                tool_name="replace_string_in_file",
                tool_input={
                    "filePath": (self.workspace_root / "projects/shared/spec-code.c4").as_posix(),
                    "oldString": "old",
                    "newString": "new",
                },
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(output), "deny")


if __name__ == "__main__":
    unittest.main()
