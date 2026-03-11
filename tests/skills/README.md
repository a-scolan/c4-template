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

At the shared `tests/skills/` root, the runner also writes:

- `skills-overview.json`
- `skills-overview.md`
- `skills-overview.html`

## Important rules

- Never keep a `SKILL.md` inside a test workspace.
- If a baseline snapshot is needed, use `BASELINE_SKILL.md` only.
- Reuse the same workspace folder for later iterations and add the next `iteration-N/` there.
- Treat these folders as evaluation evidence, not as active skills.

## MVP runner

Use `tests/run_skill_evals.py` for local replays.

What it does:

- runs through `gh copilot -- -p ...` rather than the editor agent
- isolates `HOME`, `USERPROFILE`, and `COPILOT_HOME` per run to reduce leakage from `~/.copilot/` and `~/.claude/`
- re-injects MCP servers from `~/.vscode/mcp.json` when available
- keeps the runner itself OS-independent by using Python `pathlib`, `tempfile`, and `subprocess`

Examples:

```bash
python tests/run_skill_evals.py create-element
python tests/run_skill_evals.py create-element --eval-ids 0 1 --configs with_skill without_skill
python tests/run_skill_evals.py create-element --without-skill-mode no-repo-skills
python tests/run_skill_evals.py all
python tests/run_skill_evals.py all --report-only
```

By default, `without_skill` hides only the target skill. Use `--without-skill-mode no-repo-skills` if you want a stricter repository-local baseline.

The runner always refreshes:

- a per-workspace history across all `iteration-N/benchmark.json` files
- a global multi-skill overview across all workspaces under `tests/skills/`

Use `--report-only` when you want to rebuild those reports without paying for another round of Copilot executions.
