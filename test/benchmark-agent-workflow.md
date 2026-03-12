# Benchmark Agent Workflow

This guide documents the custom benchmark agents and the shared hook policy used to keep the skill benchmark more **in vitro**.

## Required setup

- Enable `chat.useCustomAgentHooks = true` in VS Code.
- Keep using the physical relocation step for the full `without_skill` batch.
- Treat the hook policy as additive protection, not as a replacement for relocation.

## Agent inventory

| Agent file | Role | Tools | Subagents |
| --- | --- | --- | --- |
| `.github/agents/skill-benchmark-manager.agent.md` | Orchestrates the benchmark workflow and benchmark-specific documentation work | `read`, `search`, `edit`, `execute`, `todo`, `agent` | Only the constrained benchmark workers |
| `.github/agents/skill-benchmark-baseline.agent.md` | Executes the `without_skill` phase in a fresh read-only worker | `read`, `search`, `todo` | None (`agents: []`) |
| `.github/agents/skill-benchmark-with-skill.agent.md` | Executes the `with_skill` phase in a fresh read-only worker locked to one target skill | `read`, `search`, `todo` | None (`agents: []`) |
| `.github/agents/skill-blind-comparator.agent.md` | Compares blinded `A.md` vs `B.md` without seeing mapping or raw non-blind artifacts | `read`, `search`, `todo` | None (`agents: []`) |

## Shared hook engine

- Script: `.github/agents/scripts/enforce-test-access.py`
- Main hook event: `PreToolUse`
- Context injection: `SessionStart`
- Manager reinforcement: `SubagentStart`

### Policy modes

| Mode | Purpose | Main guardrails |
| --- | --- | --- |
| `benchmark_manager` | Orchestrate benchmark work and benchmark-specific docs | Can delegate only to allowlisted benchmark workers; edits are limited to `README.md`, `test/`, and `.github/agents/*.agent.md`; no shell escape |
| `baseline` | Clean `without_skill` worker | No `SKILL.md`, no edits, no terminal, no subagents |
| `with_skill_targeted` | Clean `with_skill` worker | First workspace skill read locks the session to that one skill; no edits, no terminal, no subagents |
| `blind_compare` | Blind A/B judge | May read only blind A/B artifacts and target `evals.json`; no `blind-map.json`, no raw outputs, no `SKILL.md` |

## Critical subagent rule

Constraint propagation is intentional and strict:

1. The manager may only delegate to explicit allowlisted benchmark worker agents.
2. Each worker agent sets `agents: []`, so a worker cannot chain into a looser subagent.
3. Each worker custom agent defines its own read/search tool list and its own agent-scoped hooks.
4. If a future helper subagent is introduced, it must reuse the same shared hook engine with an equal or stricter policy before it becomes eligible for delegation.

In short: **no unconstrained subagent hops are allowed anywhere in the benchmark flow.**

## What inherits, and what does not

VS Code's subagent model is subtle here:

- By default, a subagent inherits the main session's agent/model/tools.
- When you invoke a **custom agent** as a subagent, that custom agent's own model/tools/instructions override the inherited defaults.
- Agent-scoped hooks run when that custom agent is active, including when it is invoked as a subagent.

So the guarantee is **not** "the parent automatically imposes its exact hooks on the child".
The guarantee we implement is stronger and more explicit: the manager is only allowed to launch worker agents that already define the same or stricter file-access policy themselves.

## Why there are repo custom agents in addition to `skill-creator`

This is intentional.

- The files under `skill-creator/agents/*.md` are **bundled playbooks** shipped inside a skill.
- They are excellent methodological assets (`comparator.md`, `analyzer.md`, `grader.md`), but they are **not** VS Code `.agent.md` custom agents and therefore are **not** an enforcement boundary for tools or hooks.
- The repo-level benchmark agents exist to provide the missing enforcement layer: explicit tool lists, explicit subagent allowlists, and agent-scoped hooks.

The benchmark manager may consult the support skills `skill-creator` and `writing-skills`, but the measured benchmark workers remain isolated repo custom agents.

## Using the helper commands

Use the harness helpers to keep the workflow repeatable:

```bash
python test/scripts/skill_suite_tools.py agent-plan --iteration test/iteration-2
python test/scripts/skill_suite_tools.py agent-plan --iteration test/iteration-2 --skill create-element
python test/scripts/skill_suite_tools.py validate-blind-isolation --iteration test/iteration-2
python -m pytest test/scripts/test_benchmark_agent_policy.py
```

## Diagnostics

- Open the **GitHub Copilot Chat Hooks** output channel to inspect hook decisions.
- Use `#debugEventsSnapshot` when you want to inspect the effective tool payloads seen by the hooks.
- If the local schema still flags `hooks` in `.agent.md`, verify your VS Code version and keep `chat.useCustomAgentHooks = true`; the feature is preview-only in VS Code 1.111.

## Boundary of trust

- Physical relocation remains the strict guarantee for the baseline phase.
- Agent-scoped hooks reduce accidental leakage and keep comparator discipline tight.
- Do not claim hook-only isolation is sufficient until repeated benchmark runs prove it in practice.
