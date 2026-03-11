### Periodic Synchronization

For projects using this template, pull updates quarterly or when specifications change.

**Three things to always update from the template:**

1. **Copilot instructions and skills** (`.github/`)
2. **Shared specifications** (`projects/shared/`)
3. **Example project** (`projects/spec-showcase/`)

#### Recommended: Direct Checkout Method (Simpler)

```bash
# Fetch latest from template
git fetch c4-template main

# Update the three essentials
git checkout c4-template/main -- .github/copilot-instructions.md .github/skills/
git checkout c4-template/main -- projects/shared/
git checkout c4-template/main -- projects/spec-showcase/

# Review and commit
git add .github/ projects/shared/ projects/spec-showcase/
git commit -m "sync: update template files (copilot instructions, skills, specs, examples)"
git push
```

This method is simpler because it only pulls the specific files you need without full subtree history tracking.

#### Alternative: Git Subtree Method (Full History)

If you want to preserve complete history of template changes:

```bash
# Fetch latest
git fetch c4-template main

# Pull updates for each subtree with squashed history
git subtree pull --prefix=.github c4-template main --squash
git subtree pull --prefix=projects/shared c4-template main --squash
git subtree pull --prefix=projects/spec-showcase c4-template main --squash

# Review and push
git push
```

#### What Gets Updated

| Path | Files | Purpose |
|---|---|---|
| `.github/copilot-instructions.md` | Copilot workflow guidance | How Copilot should work in your project |
| `.github/skills/` | 14 skill files | Architecture helpers for Copilot |
| `projects/shared/spec-*.c4` | 6 specification files | Reusable element kinds, tags, relationships |
| `projects/shared/images/` | 28+ SVG icons | Shared architecture diagrams |
| `projects/spec-showcase/` | Example C4 diagrams | Reference examples |

**Important:** Always update all three directories together so your project stays in sync with the template's specification standards.

**Note:** The `--squash` flag (git subtree only) consolidates all c4-template changes into one commit per sync. Updates are manual—they do not happen automatically.

#### When to Sync

- **Quarterly:** Regular maintenance to stay current
- **When template skills improve:** Better Copilot assistance
- **When specs are updated:** Align with latest conventions
- **When new icons added:** More diagram options

## Skill Evaluation Workspaces

Live skills stay under `.github/skills/`. Generated evaluation artifacts and reports live under `tests/skills/`.

### Why this separation exists

- Prevent test workspaces from being discovered as active skills during handoffs
- Keep `benchmark.json`, `benchmark.md`, `review.html`, and iteration outputs out of the live skill namespace
- Make future re-runs easier from one dedicated root test area

### Convention

- Live skill source: `.github/skills/<skill-name>/`
- Evaluation workspace: `tests/skills/<skill-name>-workspace/`
- Iterations: `tests/skills/<skill-name>-workspace/iteration-N/`
- Optional baseline snapshots: `tests/skills/<skill-name>-workspace/skill-snapshot/BASELINE_SKILL.md`

### MVP runner

The repository now includes an OS-independent runner at `tests/run_skill_evals.py`.

It:

- executes prompts via `gh copilot -- -p ...`
- isolates `HOME`, `USERPROFILE`, and `COPILOT_HOME` per run to reduce user-global skill leakage
- can re-inject MCP servers from `~/.vscode/mcp.json` so isolated runs still have access to the same VS Code MCP setup

Typical usage:

```bash
python tests/run_skill_evals.py create-element
python tests/run_skill_evals.py create-element --eval-ids 0 1 --configs with_skill without_skill
python tests/run_skill_evals.py create-element --without-skill-mode no-repo-skills
python tests/run_skill_evals.py all --report-only
```

The runner now also refreshes aggregated reports from the persisted workspaces:

- per-skill workspace history:
	- `tests/skills/<skill-name>-workspace/workspace-history.json`
	- `tests/skills/<skill-name>-workspace/workspace-history.md`
	- `tests/skills/<skill-name>-workspace/workspace-history.html`
- global multi-skill overview:
	- `tests/skills/skills-overview.json`
	- `tests/skills/skills-overview.md`
	- `tests/skills/skills-overview.html`

Use `all` to run every skill with eval definitions. Use `--report-only` to regenerate the workspace/global reports from existing iteration benchmarks without launching fresh Copilot runs.

### Relationship to `skill-creator`

The evaluation workflow in this repository intentionally borrows ideas from Anthropic's [`skill-creator`](https://skills.sh/anthropics/skills/skill-creator):

- iteration-based workspaces
- `with_skill` / `old_skill` / `without_skill` comparisons
- persisted `benchmark.json` / `benchmark.md` / review artifacts
- human review after automated comparison

However, `skill-creator` is treated here as **methodology for the harness/operator**, not as a skill that should be exposed inside the measured sandbox.

Why? Because enabling `skill-creator` during the evaluated run would contaminate the measurement: it teaches how to orchestrate and judge skill tests, not how to solve the benchmark task itself. The benchmark should measure the target skill's effect, not the side effects of a meta-skill about testing.

**Important:** Never keep a `SKILL.md` inside a test workspace. Only live skill definitions belong in `.github/skills/`.

For local details and examples, see `tests/skills/README.md`.
For the hardened skill-testing specification, see `tests/SKILL_TESTING_METHODOLOGY_SPEC.md`.

## Project-Specific READMEs

This README documents the template. When creating a **project-specific repository** (e.g., for a domain like NiceLabel, banking, healthcare), create a project-specific README that:

1. Documents your architecture and systems
2. Describes how you've configured template synchronization
3. Lists which Copilot skills apply to your domain
4. Includes project-specific best practices
5. Documents your ADRs and key architectural decisions