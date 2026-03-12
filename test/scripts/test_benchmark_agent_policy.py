from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK_SCRIPT = ROOT / ".github" / "agents" / "scripts" / "enforce-test-access.py"
FIXTURES = ROOT / "test" / "scripts" / "fixtures" / "benchmark-agent-hooks"


class BenchmarkAgentPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace_root = ROOT
        self.state_root = tempfile.TemporaryDirectory()
        self.addCleanup(self.state_root.cleanup)

    def run_hook(self, fixture_name: str, *, mode: str, extra_env: dict[str, str] | None = None) -> dict:
        payload = json.loads((FIXTURES / fixture_name).read_text(encoding="utf-8"))
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

    def decision(self, output: dict) -> str:
        return output["hookSpecificOutput"]["permissionDecision"]

    def test_baseline_allows_readme(self) -> None:
        output = self.run_hook("baseline-read-readme.json", mode="baseline")
        self.assertEqual(self.decision(output), "allow")

    def test_baseline_denies_skill_reads(self) -> None:
        output = self.run_hook("baseline-deny-skill.json", mode="baseline")
        self.assertEqual(self.decision(output), "deny")

    def test_manager_allows_only_allowlisted_subagents(self) -> None:
        output = self.run_hook(
            "manager-allow-subagent.json",
            mode="benchmark_manager",
            extra_env={
                "BENCH_ALLOWED_AGENTS": "Skill Benchmark Baseline,Skill Benchmark With Skill,Skill Blind Comparator"
            },
        )
        self.assertEqual(self.decision(output), "allow")

    def test_manager_denies_unconstrained_subagents(self) -> None:
        output = self.run_hook(
            "manager-deny-subagent.json",
            mode="benchmark_manager",
            extra_env={
                "BENCH_ALLOWED_AGENTS": "Skill Benchmark Baseline,Skill Benchmark With Skill,Skill Blind Comparator"
            },
        )
        self.assertEqual(self.decision(output), "deny")

    def test_manager_may_read_allowed_support_skills_only(self) -> None:
        allowed = self.run_hook(
            "manager-read-support-skill.json",
            mode="benchmark_manager",
            extra_env={"BENCH_SUPPORT_SKILLS": "skill-creator,writing-skills"},
        )
        self.assertEqual(self.decision(allowed), "allow")

        denied = self.run_hook(
            "worker-read-support-skill.json",
            mode="baseline",
            extra_env={"BENCH_SUPPORT_SKILLS": "skill-creator,writing-skills"},
        )
        self.assertEqual(self.decision(denied), "deny")

    def test_with_skill_locks_first_skill_directory(self) -> None:
        first = self.run_hook("with-skill-read-target-skill.json", mode="with_skill_targeted")
        self.assertEqual(self.decision(first), "allow")

        second = self.run_hook("with-skill-read-other-skill.json", mode="with_skill_targeted")
        self.assertEqual(self.decision(second), "deny")

    def test_blind_comparator_denies_mapping_file(self) -> None:
        output = self.run_hook("blind-deny-map.json", mode="blind_compare")
        self.assertEqual(self.decision(output), "deny")

    def test_blind_comparator_allows_blind_artifacts_and_evals(self) -> None:
        blind = self.run_hook("blind-read-a.json", mode="blind_compare")
        self.assertEqual(self.decision(blind), "allow")

        evals = self.run_hook("blind-read-evals.json", mode="blind_compare")
        self.assertEqual(self.decision(evals), "allow")

    def test_manager_command_allowlist_blocks_shell_escape(self) -> None:
        output = self.run_hook("manager-deny-command.json", mode="benchmark_manager")
        self.assertEqual(self.decision(output), "deny")


if __name__ == "__main__":
    unittest.main()
