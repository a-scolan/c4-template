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
- Prefer discriminating eval prompts and assertions: require canonical minimal fixes, explicit rule verdicts for invalid outputs, and ambiguity-resistant cases rather than broad prose-only answers.
- Re-check domain truth-claims against authoritative semantics before changing prompts or expectations; when near-miss syntax matters, prefer contrastive wording over vague prose.
- Comparator-only grading tie-breaks may live in optional hidden `grading-spec.json` fields such as `grading_guidance`; keep those details out of public prompts.
- Grader-only executable verification hints may live in hidden `grading-spec.json` via optional `default_execution_checks` (skill-level defaults) and/or eval-level `execution_checks`; effective checks are merged per eval, and non-executable evals must remain fully supported.
- Run `pre-aggregate-check` before the final `aggregate` step so missing summaries / blind comparisons fail fast instead of being silently skipped.
- Prefer `resume-finalize` for interruption recovery: it auto-materializes missing `blind-comparisons.json` from raw comparison journals under `test/<iteration>/_meta/raw-comparison-*.json`, runs `pre-aggregate-check`, then writes fresh suite summaries.
- For blind comparison, prefer worker-side journaling: `blind-compare-bundle` now provides a per-task `raw_output_path`, and comparator workers should write their wrapped JSON to `test/<iteration>/_meta/raw-comparison-*.json` before returning a tiny acknowledgment.
- Keep all canonical outputs under `test/<iteration>/`.
- Treat review exports and hook traces as disposable by default.
- Prefer JSON as the machine source of truth; `suite-summary.md` remains the human-facing rendering of suite results.
- For each benchmarked skill, complete a mandatory Anthropic skill-authoring best-practices pass in `test/<iteration>/<skill>/synthesis.md` (concision, degrees-of-freedom fit, triggerability metadata quality, progressive disclosure quality, workflow/validation loop quality, anti-pattern scan with prioritized fixes).
- For LikeC4 DSL evals specifically, apply an implicit test-context contract when a prompt does not fully define project specification: assume a minimal valid LikeC4 context consistent with official semantics (nearest-config project scope, allowed top-level blocks, lexical scoping/FQN rules, and explicitly referenced kinds/tags). Do not penalize answers that make these assumptions explicit before solving.

### Resilient benchmark flow

The benchmark harness now aims to be interruption-tolerant rather than interruption-free:

- JSON writes use atomic replacement, reducing the chance of half-written benchmark artifacts.
- Large blind-comparison payloads are now expected to be journaled directly under `test/<iteration>/_meta/raw-comparison-*.json` instead of relying on large chat responses.
- `pre-aggregate-check` validates that each skill has both summaries, both run-metrics files, and `blind-comparisons.json` before a final suite aggregation.
- `resume-finalize` provides a deterministic one-step recovery/finalization path (`materialize missing blind artifacts -> pre-check -> aggregate`) after interruptions.
- `suite-summary.json` now reports `skipped_skills` explicitly when partial artifacts are still present, instead of silently hiding omissions.
- Manager workflows should persist every blind comparator result immediately with `materialize-comparisons` rather than relying on deferred manual writeback.

### Trace policy

Benchmark agents now default to `BENCH_TRACE_LEVEL=normal`, so normal runs do not emit hook logs.

Escalate only when needed:

- `audit`: resolved decisions only
- `debug`: raw debug log + resolved audit log

### Cleanup helpers

Useful helpers:

- `clean-benchmark-artifacts` removes generated iterations, hook traces, probe folders, and Python cache
- `prune-generated-artifacts` removes disposable per-iteration review exports such as `_skill-creator-review-workspace/`, `skill-creator-review.html`, and `skill-creator-benchmark.json`

### Python test launch reliability (Windows + venv)

To avoid intermittent `ModuleNotFoundError: No module named 'test.scripts'` when launching tests with dotted module names, prefer discovery mode from the repository root:

- `python -m unittest discover -s test/scripts/tests -p "test_*.py"`

The repository now also exposes `test/`, `test/scripts/`, and `test/scripts/tests/` as Python packages for better compatibility with dotted module invocations.

For the full benchmark protocol and rationale, read `test/benchmark-agent-workflow.md`.