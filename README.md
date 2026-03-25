### Periodic Synchronization

For projects using this template, pull updates quarterly or when specifications change.

**Core things to keep in sync from the upstream template:**

1. **Copilot instructions and skills** (`.github/`)
2. **Shared specifications** (`projects/shared/`)
3. **Example project** (`projects/spec-showcase/`) when you want refreshed human-facing examples

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
| `projects/spec-showcase/` | Example C4 diagrams | Pedagogical examples for humans |

**Important:** `.github/` and `projects/shared/` are the main automation-facing sync surfaces. Example projects such as `projects/spec-showcase/` and `projects/template/` are useful pedagogical assets, but they should not be treated as sources of truth for skills or eval behavior.

**Note:** The `--squash` flag (git subtree only) consolidates all c4-template changes into one commit per sync. Updates are manual—they do not happen automatically.

#### When to Sync

- **Quarterly:** Regular maintenance to stay current
- **When template skills improve:** Better Copilot assistance
- **When specs are updated:** Align with latest conventions
- **When new icons added:** More diagram options

## Project-Specific READMEs

This README documents the template. When creating a **project-specific repository** (e.g., for a domain like NiceLabel, banking, healthcare), create a project-specific README that:

1. Documents your architecture and systems
2. Describes how you've configured template synchronization
3. Lists which Copilot skills apply to your domain
4. Includes project-specific best practices
5. Documents your ADRs and key architectural decisions


## Skill Benchmarking

This repository includes a controlled benchmark harness for evaluating one skill against a strict baseline.

Use:

- human entrypoint: workspace agent `Skill Benchmark Manager`
- automation entrypoint: `python test/scripts/skill_suite_tools.py self-test --iteration test/iteration-N --workspace-root .`
- canonical benchmark guide: `test/benchmark-agent-workflow.md`

The benchmark guide now centralizes workflow, trust rules, hook modes, trace levels, canonical outputs, and review exports.

### Minimal operating rules

- Use the strict relocated baseline by default.
- Run workers in parallel only within a phase.
- Keep `without_skill`, `with_skill`, and `blind_compare` strictly sequential across phases.
- Keep all canonical outputs under `test/<iteration>/`.
- Treat review exports and hook traces as disposable by default.
- Prefer JSON as the machine source of truth; `suite-summary.md` remains the human-facing rendering of suite results.

### Trace policy

Benchmark agents now default to `BENCH_TRACE_LEVEL=normal`, so normal runs do not emit hook logs.

Escalate only when needed:

- `audit`: resolved decisions only
- `debug`: raw debug log + resolved audit log

### Cleanup helpers

Useful helpers:

- `clean-benchmark-artifacts` removes generated iterations, hook traces, probe folders, and Python cache
- `prune-generated-artifacts` removes disposable per-iteration review exports such as `_skill-creator-review-workspace/`, `skill-creator-review.html`, and `skill-creator-benchmark.json`

For the full benchmark protocol and rationale, read `test/benchmark-agent-workflow.md`.