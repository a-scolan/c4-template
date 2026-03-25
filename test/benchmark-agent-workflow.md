# Benchmark Agent Workflow

This guide documents the custom benchmark agents and the shared hook policy used to keep the skill benchmark more **in vitro**.

## Required setup

- Keep `.vscode/settings.json` committed with `chat.useCustomAgentHooks = true` so the workspace enables benchmark hooks by default.
- Use the strict relocated baseline by default for the full `without_skill` batch.
- Run independent workers in parallel by default **within** each phase.
- Treat the hook-only baseline worker as an explicit probe mode, not as a replacement for relocation.
- If resolved hook-audit entries show that raw `sessionId` is missing, confirm effective anonymous session ids are derived per worker scope (`with_skill`: per skill, `blind_compare`: per iteration+skill). If derivation is missing or ambiguous, reset anonymous hook state and temporarily serialize the affected stateful phase.
- Before the first scored worker of a campaign, run a live isolation probe against a clearly forbidden file (for example `README.md` or a prior-iteration artifact) and confirm the worker is truly blocked.
- Regenerate `suite-summary.json` and `suite-summary.md` for the active iteration after each blind-comparison materialization (treat this as mandatory, not optional post-processing).

## Entry points

- **Human / interactive entrypoint**: use the workspace custom agent `Skill Benchmark Manager`.
- **Automation / offline entrypoint**: run `python test/scripts/skill_suite_tools.py self-test --iteration test/iteration-N --workspace-root .`.

The other `skill_suite_tools.py` subcommands are low-level harness helpers. They remain useful for reproducibility and automation, but they are not the day-to-day starting point for humans.

## Default parallel dispatch policy

Use this scheduler unless a run-specific constraint forces a narrower scope:

1. Build a task matrix for the current phase (`without_skill`, `with_skill`, or `blind_compare`).
2. Launch the whole matrix in parallel waves, as long as output directories do not overlap.
3. Wait for all workers in the phase to finish (phase barrier).
4. Start the next phase only after the previous one is fully complete.

This means the benchmark is **parallel by default inside a phase** and **strictly sequential across phase boundaries**.

If the live hook payloads omit `sessionId`, the wrapper derives anonymous session state from requested scope for stateful modes (`with_skill_targeted`: per skill; `blind_compare`: per iteration+skill), which keeps independent workers parallel-safe. If a worker cannot be mapped to a stable scope, fall back to serial execution for that phase and clear anonymous hook state between fresh workers.

## Agent inventory

| Agent file | Role | Tools | Subagents |
| --- | --- | --- | --- |
| `.github/agents/skill-benchmark-manager.agent.md` | Orchestrates the benchmark workflow and benchmark-specific documentation work | `read`, `search`, `edit`, `execute`, `todo`, `agent` | Only the constrained benchmark workers |
| `.github/agents/skill-benchmark-baseline.agent.md` | Executes the strict relocated `without_skill` phase in a fresh read-only worker | `read`, `search`, `todo` | None (`agents: []`) |
| `.github/agents/skill-benchmark-baseline-hook-only.agent.md` | Executes an experimental hook-only `without_skill` probe without relocating workspace skills | `read`, `search`, `todo` | None (`agents: []`) |
| `.github/agents/skill-benchmark-with-skill.agent.md` | Executes the `with_skill` phase in a fresh read-only worker locked to one target skill | `read`, `search`, `todo` | None (`agents: []`) |
| `.github/agents/skill-blind-comparator.agent.md` | Compares blinded `A.md` vs `B.md` without seeing mapping or raw non-blind artifacts | `read`, `search`, `todo` | None (`agents: []`) |

## Shared hook engine

- Script: `test/scripts/benchmark_access_hook.py`
- Main hook event: `PreToolUse`
- Context injection: `SessionStart`
- Manager reinforcement: `SubagentStart`

The wrapper under `test/scripts/benchmark_access_hook.py` is the active benchmark hook entrypoint. It reuses the legacy policy logic while resetting stale session state on `SessionStart`, deriving missing `sessionId` values into per-scope anonymous session ids for stateful modes, avoiding false path detection in `create_file` payload content, and letting blind-comparator sessions lock onto the first requested iteration instead of whichever iteration folder happens to sort last.

When hook debug logging is enabled, the wrapper also writes a resolved audit trail beside the raw attempt log so you can distinguish blocked attempts from actually allowed tool uses and compare raw vs effective session ids.

### Policy modes

| Mode | Purpose | Main guardrails |
| --- | --- | --- |
| `benchmark_manager` | Orchestrate benchmark work and benchmark-specific docs | Can delegate only to allowlisted benchmark workers; edits are limited to `README.md`, `test/`, and `.github/agents/*.agent.md`; no shell escape; no MCP |
| `baseline` | Strict relocated `without_skill` worker | Requires `.github/skills/` to be empty before tool use; worker reads are limited to `projects/shared/`; all LikeC4 MCP tools (`likec4/*`) allowed; no `SKILL.md`, no `README.md`, no project-local examples, no `test/` artefacts, no edits, no terminal, no subagents |
| `baseline_hook_only` | Hook-only `without_skill` isolation probe | Workspace skills may remain in place, but worker reads are still limited to `projects/shared/`; all LikeC4 MCP tools (`likec4/*`) allowed; no `.github` path, no `_disabled-skills` backup, no `SKILL.md`, no `README.md`, no project-local examples, no edits, no terminal, no subagents |
| `with_skill_targeted` | Clean `with_skill` worker | First workspace skill read locks the session to that one skill; inside that skill, benchmark prompts must come from `evals/evals-public.json` only; outside that skill, worker reads are limited to `projects/shared/`; all LikeC4 MCP tools (`likec4/*`) allowed; no unrelated `test/` artefacts, no edits, no terminal, no subagents. If raw `sessionId` is missing, the wrapper derives a skill-scoped anonymous session id so parallel workers stay isolated; if this cannot be derived, reset hook state and serialize as fallback. |
| `blind_compare` | Blind A/B judge | May read only blind A/B artifacts and target `grading-spec.json`; no `blind-map.json`, no raw outputs, no `SKILL.md`; no MCP, including LikeC4 MCP. The comparator locks to the first blind iteration/skill it touches instead of assuming the numerically latest iteration folder. If raw `sessionId` is missing, the wrapper derives iteration+skill-scoped anonymous session ids to preserve parallelism; if this cannot be derived, reset hook state and serialize as fallback. |

LikeC4 MCP is intentionally allowed only for the scored answer-generation workers (`baseline`, `baseline_hook_only`, and `with_skill_targeted`) because some LikeC4 tasks need model and relationship grounding even in `without_skill`. That allowance is deliberately narrow: keep it to element/relationship grounding only. Project listing, project summaries, and view browsing are blocked during scored runs because they expose template/showcase examples outside `projects/shared/`. LikeC4 MCP remains blocked for `benchmark_manager` and `blind_compare`, and the grader/analyzer support playbooks are not part of this MCP allowance.

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

The benchmark manager may consult the workspace skill `skill-creator`, but the measured benchmark workers remain isolated repo custom agents.

Outside the locked skill, benchmark workers are intentionally allowed to read only `projects/shared/` because those files act as reusable specification examples. They may not consult `README.md`, `projects/template/`, or `projects/spec-showcase/` during scored runs.

## Provisional iterations and forbidden fallback

Never reuse `blind-comparisons.json` from a previous iteration as if it were fresh comparator evidence for the current iteration. Those judgments belong to older outputs and can silently invalidate blind-derived metrics and previous-iteration deltas.

If the blind-comparison phase cannot be completed cleanly:

1. keep the current iteration marked as provisional,
2. write machine-readable caveats to `test/iteration-N/_meta/benchmark-caveats.json`,
3. suppress previous-iteration comparison in the aggregated report,
4. rerun the comparator phase later instead of copying old comparison payloads forward.

Use the same caveat file when timings are synthetic placeholders or when `with_skill` had to fall back to injected guidance.

The scored protocol is now versioned. Before a campaign, freeze the active agent prompts, hook rules, and split eval artifacts into `test/iteration-N/_meta/protocol-lock.json` with `skill_suite_tools.py protocol-preflight`.

When writing synthesis text, do not over-claim from one eval disagreement. If a single eval loses while suite-level metrics remain strong, report it as a focused disagreement to verify (comparator reasoning vs grading spec vs DSL semantics), not as a blanket skill failure.

## Support playbook mapping

| Support playbook | Used by | Purpose |
| --- | --- | --- |
| `skill-creator/agents/comparator.md` | Benchmark manager + blind comparator workflow | Blind A/B judging style, rubric framing, decisive winner selection |
| `skill-creator/agents/analyzer.md` | Benchmark manager | Post-hoc pattern analysis across benchmark outputs |
| `skill-creator/agents/grader.md` | Benchmark manager | Evaluating expectation quality and spotting weak assertions |
| `skill-creator/eval-viewer/generate_review.py` | Benchmark manager | Generate a human-review HTML from exported benchmark outputs |
| `skill-creator/references/schemas.md` | Benchmark manager | Keep exported `benchmark.json` and review workspace layouts compatible with the viewer |

## Using the helper commands

Recommended starting points:

```bash
python test/scripts/skill_suite_tools.py clean-benchmark-artifacts --workspace-root .
python test/scripts/skill_suite_tools.py utc-now
python test/scripts/skill_suite_tools.py self-test --iteration test/iteration-2 --workspace-root .
python test/scripts/skill_suite_tools.py write-protocol-manifest --workspace-root .
python test/scripts/skill_suite_tools.py protocol-preflight --iteration test/iteration-2 --workspace-root .
python test/scripts/skill_suite_tools.py validate-hook-audit --path test/_agent-hooks/hook-audit.jsonl --mode baseline
python test/scripts/skill_suite_tools.py reset-hook-state --workspace-root . --mode with_skill_targeted
python test/scripts/skill_suite_tools.py reset-hook-state --workspace-root . --mode blind_compare
python test/scripts/skill_suite_tools.py agent-plan --iteration test/iteration-2 --baseline-isolation relocation
python test/scripts/skill_suite_tools.py agent-plan --iteration test/iteration-2 --baseline-isolation hook-only
```

Low-level helper commands remain available when you need them:

```bash
python test/scripts/skill_suite_tools.py agent-plan --iteration test/iteration-2 --skill create-element
python test/scripts/skill_suite_tools.py blind-compare-bundle --iteration test/iteration-2 --workspace-root . --skill create-element --eval-id 0
python test/scripts/skill_suite_tools.py blind-compare-bundle --iteration test/iteration-2 --workspace-root . --skill create-element --eval-id 0 --run-number 2
python test/scripts/skill_suite_tools.py analyzer-bundle --iteration test/iteration-2 --workspace-root . --skill create-element
python test/scripts/skill_suite_tools.py grader-bundle --iteration test/iteration-2 --workspace-root . --skill create-element --eval-id 0 --configuration with_skill
python test/scripts/skill_suite_tools.py materialize-run --iteration test/iteration-2 --skill create-element --configuration with_skill --raw-json test/iteration-2/_meta/create-element-with_skill.json --run-number 2
python test/scripts/skill_suite_tools.py materialize-comparisons --iteration test/iteration-2 --skill create-element --raw-json test/iteration-2/_meta/create-element-blind.json
python test/scripts/skill_suite_tools.py validate-executable-checks --iteration test/iteration-2 --workspace-root .
python test/scripts/skill_suite_tools.py export-review-workspace --iteration test/iteration-2 --workspace-root . --skill create-element
python test/scripts/skill_suite_tools.py write-skill-creator-benchmark --iteration test/iteration-2 --workspace-root . --skill create-element
python test/scripts/skill_suite_tools.py write-static-review --iteration test/iteration-2 --workspace-root . --skill create-element
python test/scripts/skill_suite_tools.py validate-blind-isolation --iteration test/iteration-2
python test/scripts/test_benchmark_agent_policy.py
```

`materialize-comparisons` now refreshes per-config summaries and rewrites `suite-summary.json` + `suite-summary.md` for the same iteration automatically.

Use `utc-now` immediately before and after a scored worker when you need auditable per-worker timestamps without leaving the benchmark-manager command allowlist.

When raw `sessionId` is missing in live hook-audit entries, inspect `effectiveSessionId` in the resolved hook audit: parallel stateful dispatch is acceptable when those ids stay distinct per worker scope. Use `reset-hook-state` to clear stale anonymous files between campaigns or before forcing a serialized fallback.

## Skill-creator-aligned review flow

1. Use `export-review-workspace` to adapt one benchmarked skill into the directory layout expected by `skill-creator`'s review viewer.
2. Use `write-skill-creator-benchmark` to export a viewer-compatible `benchmark.json` without inventing token counts when they were never captured.
3. Use `write-static-review` to invoke `skill-creator/eval-viewer/generate_review.py` and write a standalone HTML file under `test/`, including the benchmark tab.
4. Use `grader-bundle` when you want a run-level grading handoff in the style of `skill-creator/agents/grader.md`.
5. Use `analyzer-bundle` when preparing a benchmark-analysis task in the style of `skill-creator/agents/analyzer.md`.

This keeps the benchmark workflow inside the same evaluation family as `skill-creator`, instead of creating a parallel review system.

The support skill `.github/skills/skill-creator/` is intentionally vendored and versioned here. The exported review workspaces and HTML/benchmark files produced from it are generated artifacts under `test/` and should normally be regenerated rather than committed.

## Diagnostics

- Open the **GitHub Copilot Chat Hooks** output channel to inspect hook decisions.
- Use `#debugEventsSnapshot` when you want to inspect the effective tool payloads seen by the hooks.
- The default debug log target is `test/_agent-hooks/hook-debug.jsonl`; rotate or delete it between campaigns when needed.
- The resolved decision log lives beside it at `test/_agent-hooks/hook-audit.jsonl`; use `validate-hook-audit` to confirm that scored workers only received allowed reads and that broad LikeC4 MCP browsing stayed denied.
- If `validate-hook-audit` reports malformed JSONL lines, treat the audit log as disposable campaign state: rotate or delete `test/_agent-hooks/` and rerun the affected phase instead of trusting a partially corrupted log.
- If the local schema still flags `hooks` in `.agent.md`, verify your VS Code version and keep `chat.useCustomAgentHooks = true`; the feature is preview-only in VS Code 1.111.

## Boundary of trust

- Physical relocation remains the strict guarantee for the baseline phase.
- Agent-scoped hooks reduce accidental leakage and keep comparator discipline tight.
- Hook-only baseline runs are useful probes, but do not claim they are sufficient until repeated benchmark runs prove it in practice.
