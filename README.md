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


## Skill Benchmarking

This repository includes a controlled benchmark harness for evaluating one skill against a strict baseline.
The benchmark is designed to answer three questions:

1. **Does the skill improve answer quality?**
2. **What extra cost does it introduce?**
3. **Can the comparison be trusted?**

Quality is measured through hidden grading expectations, blind A/B comparison, and automated LikeC4 snippet checks. Cost is tracked through run metrics and suite summaries. Trust comes from strict isolation rules for the baseline, prompt-only `evals-public.json` access for the `with_skill` phase, hidden `grading-spec.json` access for blind comparison only, a frozen protocol manifest per iteration, tightly limited shared-spec access outside the locked skill, and validation of the generated artefacts.

### What to use

- **Human / interactive entrypoint:** workspace custom agent `Skill Benchmark Manager`
- **Automation / offline entrypoint:** `python test/scripts/skill_suite_tools.py self-test --iteration test/iteration-N --workspace-root .`
- **Detailed implementation guide:** `test/benchmark-agent-workflow.md`
- **Benchmark protocol prompt:** `test/skill-suite-eval-prompt.md`

### Required configuration

Before running a benchmark:

- Keep the workspace setting in `.vscode/settings.json` so `chat.useCustomAgentHooks = true` is enabled by default.
- Use the **strict relocated baseline** by default.
- Run independent workers in parallel by default inside each phase, with a hard barrier between phases.
- Keep all benchmark artefacts under `test/iteration-N/`.
- Keep reports anonymous and repository-relative.

Before the first scored worker of a campaign, run one tiny live probe with the actual benchmark worker agent and confirm that a forbidden file such as `README.md` or a prior-iteration artefact is really blocked. Offline policy tests are necessary, but they are not sufficient on their own.

The hook-only baseline worker exists only for explicit isolation probes. It is useful diagnostically, but it is **not** the default trust boundary for published benchmark results.

### Recommended workflow

1. Create or select an iteration folder such as `test/iteration-3/`.
2. Ensure every target skill already exposes split eval artifacts (`evals-public.json` and `grading-spec.json`) and lock the active protocol before scored runs:
	- `python test/scripts/skill_suite_tools.py write-protocol-manifest --workspace-root .`
	- `python test/scripts/skill_suite_tools.py protocol-preflight --iteration test/iteration-N --workspace-root .`
3. Run the offline sanity check:
	- `python test/scripts/skill_suite_tools.py self-test --iteration test/iteration-N --workspace-root .`
4. Run the full `without_skill` batch **first**, after physically relocating workspace skills out of `.github/skills/`, and parallelize across independent skill workers.
5. Restore the skill directories to `.github/skills/`.
6. Run the `with_skill` batch in fresh workers created after restoration, parallelized across independent skill workers. Prefer `n >= 3` runs per `<skill, configuration>` when you want publishable claims.
7. Produce blinded `A.md` / `B.md` artefacts and evaluate them with the blind comparator.
8. Write, normalise, and validate run metrics before aggregation:
	- `python test/scripts/skill_suite_tools.py materialize-run --iteration test/iteration-N --skill <name> --configuration with_skill --raw-json test/iteration-N/_meta/<name>-with_skill.json`
	- `python test/scripts/skill_suite_tools.py materialize-comparisons --iteration test/iteration-N --skill <name> --raw-json test/iteration-N/_meta/<name>-blind.json`
	- `python test/scripts/skill_suite_tools.py write-run-metrics ...`
	- `python test/scripts/skill_suite_tools.py normalize-metrics --iteration test/iteration-N`
	- `python test/scripts/skill_suite_tools.py validate-metrics --iteration test/iteration-N`
	- `python test/scripts/skill_suite_tools.py validate-executable-checks --iteration test/iteration-N --workspace-root .`
	9. Aggregate per-skill and suite-level outputs.

If you intentionally run a hook-only baseline probe, keep its results separate from the strict relocated baseline.

### How the benchmark works

The workflow is orchestrated by custom agents under `.github/agents/`:

- `skill-benchmark-manager.agent.md` orchestrates the process.
- `skill-benchmark-baseline.agent.md` runs the strict `without_skill` phase.
- `skill-benchmark-baseline-hook-only.agent.md` runs the experimental hook-only probe.
- `skill-benchmark-with-skill.agent.md` runs the targeted `with_skill` phase.
- `skill-blind-comparator.agent.md` judges blinded outputs.

All of them rely on the shared hook engine in `.github/agents/scripts/enforce-test-access.py`.

In practice, the benchmark works like this:

- the **manager** may delegate only to constrained benchmark workers;
- the **baseline** worker must operate with `.github/skills/` emptied beforehand and may read only shared specification examples under `projects/shared/`;
- the **with-skill** worker is locked to one target skill per session, reads prompts only from `evals/evals-public.json`, and may otherwise read only shared specification examples under `projects/shared/`;
- the **blind comparator** may read only blinded artefacts plus the target `evals/grading-spec.json` entry;
- the **manager** freezes the active protocol version into `test/iteration-N/_meta/protocol-lock.json` before scored runs.

The bundled workspace skill `.github/skills/skill-creator/` is used as a methodological support skill for review/export tooling, but it is **not** the enforcement boundary. The enforcement boundary is provided by the repo custom agents and their hooks.

### Trust constraints

The benchmark is only meaningful if these constraints hold:

- No MCP tools are used by benchmark agents.
- No unconstrained subagent chaining is allowed.
- The full `without_skill` batch is executed before any `with_skill` run.
- Parallelism is intra-phase only: workers may run concurrently inside one phase, but `without_skill` and `with_skill` phases must never overlap.
- `with_skill` runs happen only after skill restoration and in fresh sessions.
- Benchmark workers do not read `README.md` or project-local examples such as `projects/template/` or `projects/spec-showcase/`; outside the target skill, repository reads are limited to `projects/shared/` as specification examples only.
- `with_skill` workers do not read hidden grading artefacts such as `grading-spec.json`; they read only `evals-public.json` for prompts.
- Benchmark workers do not read prior iteration artefacts under `test/`, except for the dedicated blind comparator reading `blind/A.md` and `blind/B.md`.
- The relocated backup under `test/iteration-N/_disabled-skills/` is never worker-readable.
- Blind comparison must stay blind to `blind-map.json`, raw `with_skill` outputs, raw `without_skill` outputs, summaries, metrics, and every `SKILL.md` file; it reads hidden grading data only from `grading-spec.json`.
- The protocol manifest and iteration lock must validate before a scored campaign starts.
- Repeated runs should be used for publishable comparisons so the suite can report variance, not just directionality.
- Metrics must be validated before suite aggregation.

If a baseline run can still see workspace skills, or if a blind-comparison worker can see non-blind artefacts, the run should be treated as contaminated and rerun.

### Outputs to keep vs regenerate

Canonical benchmark outputs live under `test/iteration-N/` and include:

- per-skill eval folders and blind artefacts;
- optional raw worker/comparator payloads under `test/iteration-N/_meta/` when you need an audit trail before materialisation;
- `with_skill-summary.json` / `without_skill-summary.json`;
- `with_skill-run-metrics.json` / `without_skill-run-metrics.json`;
- `blind-comparisons.json`;
- `with_skill-executable-checks.json` / `without_skill-executable-checks.json`;
- `_meta/metric-validation.json` and, when needed, `_meta/metric-normalization.json`;
- `_meta/protocol-lock.json` and `_meta/executable-checks-summary.json`;
- suite-level summaries such as `suite-summary.json` and `suite-summary.md`.

The support skill `.github/skills/skill-creator/` is intentionally versioned because the review/export workflow depends on it.
By contrast, generated review exports such as `test/iteration-N/<skill>/_skill-creator-review-workspace*/`, `skill-creator-review.html`, and `skill-creator-benchmark.{json,md}` are derived artefacts and should normally be regenerated locally instead of committed.


## Project-Specific READMEs

This README documents the template. When creating a **project-specific repository** (e.g., for a domain like NiceLabel, banking, healthcare), create a project-specific README that:

1. Documents your architecture and systems
2. Describes how you've configured template synchronization
3. Lists which Copilot skills apply to your domain
4. Includes project-specific best practices
5. Documents your ADRs and key architectural decisions