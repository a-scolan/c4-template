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

ROOT = Path(__file__).resolve().parents[2]
HOOK_SCRIPT = ROOT / ".github" / "agents" / "scripts" / "enforce-test-access.py"
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
        session_id: str,
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
        session_id: str,
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

    def test_baseline_allows_likec4_mcp_tools_after_relocation(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.mcp_payload(
                "baseline-mcp-session",
                "mcp_likec4_read-project-summary",
                {"project": "template"},
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_baseline_allows_additional_likec4_mcp_tools_after_relocation(self) -> None:
        self.clear_workspace_skills()
        output = self.run_hook_payload(
            self.mcp_payload(
                "baseline-mcp-extra-session",
                "mcp_likec4_element-diff",
                {"element1Id": "shop.frontend", "element2Id": "shop.backend"},
            ),
            mode="baseline",
        )
        self.assertEqual(self.decision(output), "allow")

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

    def test_baseline_hook_only_allows_likec4_mcp_tools(self) -> None:
        output = self.run_hook_payload(
            self.mcp_payload(
                "baseline-hook-mcp-session",
                "mcp_likec4_list-projects",
            ),
            mode="baseline_hook_only",
        )
        self.assertEqual(self.decision(output), "allow")

    def test_with_skill_allows_likec4_mcp_tools(self) -> None:
        output = self.run_hook_payload(
            self.mcp_payload(
                "with-skill-mcp-session",
                "mcp_likec4_search-element",
                {"search": "corePlatform"},
            ),
            mode="with_skill_targeted",
        )
        self.assertEqual(self.decision(output), "allow")

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

    def test_blind_comparator_denies_previous_iteration_blind_artifacts(self) -> None:
        output = self.run_hook_payload(
            self.read_payload("blind-old-session", "test/iteration-1/create-element/eval-0/blind/A.md", end_line=40),
            mode="blind_compare",
        )
        self.assertEqual(self.decision(output), "deny")

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


if __name__ == "__main__":
    unittest.main()
