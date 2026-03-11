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
- optional `skill-snapshot/BASELINE_SKILL.md`

## Important rules

- Never keep a `SKILL.md` inside a test workspace.
- If a baseline snapshot is needed, use `BASELINE_SKILL.md` only.
- Reuse the same workspace folder for later iterations and add the next `iteration-N/` there.
- Treat these folders as evaluation evidence, not as active skills.
