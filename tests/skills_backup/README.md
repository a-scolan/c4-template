# Skill evaluation workspaces

Generated skill-evaluation artifacts live here, isolated from the live skills under `.github/skills/`.

For the hardened testing methodology and sandboxing requirements, see `../SKILL_TESTING_METHODOLOGY_SPEC.md`.

## Convention

- Live skill source: `.github/skills/<skill-name>/`
- Evaluation workspace: `tests/skills/<skill-name>-workspace/`
- Iterations: `tests/skills/<skill-name>-workspace/iteration-N/`

## What stays in a workspace

- `iteration-N/` folders with qualitative outputs and grading
- `benchmark.json` and `benchmark.md`
- `review.html`
- `workspace-history.json`, `workspace-history.md`, `workspace-history.html`
- optional `skill-snapshot/BASELINE_SKILL.md`
- optional runner-managed `iteration-N/_support-skill-workspace/` containing a plain snapshot of `skill-creator` for grader-side methodology

At the shared `tests/skills/` root, the runner also writes:

- `skills-overview.json`
- `skills-overview.md`
- `skills-overview.html`

## Important rules

- Never keep the target skill-under-test as an active `SKILL.md` inside a test workspace.
- If a baseline snapshot is needed, use `BASELINE_SKILL.md` only.
- Reuse the same workspace folder for later iterations and add the next `iteration-N/` there.
- Treat these folders as evaluation evidence, not as active skills.
- The only allowed `skill-creator` snapshot under `tests/skills/` is the runner-managed `_support-skill-workspace/skill-creator/`, used only for grader/analyzer/comparator-style support calls and not as a discoverable repo-local skill.

## MVP runner

Use `tests/run_skill_evals.py` for local replays.

What it does:

- runs through `gh copilot -- -p ...` rather than the editor agent
- isolates `HOME`, `USERPROFILE`, and `COPILOT_HOME` per run to reduce leakage from `~/.copilot/` and `~/.claude/`
- re-injects MCP servers from `~/.vscode/mcp.json` when available
- keeps the runner itself OS-independent by using Python `pathlib`, `tempfile`, and `subprocess`
- snapshots the locally installed `skill-creator` files into `iteration-N/_support-skill-workspace/` and derives grader instructions from `agents/grader.md` there
- constrains grader runs to local evidence (`_grader_inputs/` + local `skill-creator` snapshot), without external search
- measures executor wall-clock time from the real `gh copilot` subprocess, while also storing CLI `usage.totalApiDurationMs` / `usage.sessionDurationMs` when available
- measures assistant output tokens from the CLI JSONL stream (`assistant.message.data.outputTokens`)
- writes live progress feedback to `iteration-N/progress.json` and `iteration-N/progress.log` while runs are still executing, even when the CLI emits plain text rather than JSONL events

Current GitHub CLI limitation: prompt/input token counts are not exposed in JSONL, so benchmark token totals cover assistant output only.

Examples:

```bash
python tests/run_skill_evals.py create-element
python tests/run_skill_evals.py create-element --eval-ids 0 1 --configs with_skill without_skill
python tests/run_skill_evals.py create-element --without-skill-mode no-repo-skills
python tests/run_skill_evals.py create-element --heartbeat-seconds 5
python tests/run_skill_evals.py all
python tests/run_skill_evals.py all --report-only
```

By default, `without_skill` hides only the target skill. Use `--without-skill-mode no-repo-skills` if you want a stricter repository-local baseline.

The runner always refreshes:

- per-iteration `benchmark.json`, `benchmark.md`, and `review.html` from persisted run artefacts when they are available
- a per-workspace history across all `iteration-N/benchmark.json` files
- a global multi-skill overview across all workspaces under `tests/skills/`

Use `--report-only` when you want to rebuild those reports without paying for another round of Copilot executions.

When older iterations come from the legacy static harness, missing timing/token measurements are now rendered as `-` instead of misleading `0` values.

If a run feels quiet, open `tests/skills/<skill-name>-workspace/iteration-N/progress.log` or `progress.json` to see the latest heartbeat, current eval/configuration, elapsed time, and last observed Copilot event.

## About `skill-creator`

This repo's testing flow is inspired by Anthropic's [`skill-creator`](https://skills.sh/anthropics/skills/skill-creator), especially for:

- iteration folders
- baseline comparisons
- benchmark aggregation
- human review loops

But `skill-creator` is **not** intended to be made visible inside the benchmarked sandbox itself.

It is a **meta-skill for designing and running evaluations**. If you expose it during the measured run, you risk changing the model's behavior for reasons unrelated to the target skill being benchmarked.

In other words:

- use `skill-creator` to shape the evaluation methodology
- do **not** count it as part of the skill-under-test environment
- if the runner snapshots it under `_support-skill-workspace/`, that workspace is for grader-side support only, not for the measured executor run
