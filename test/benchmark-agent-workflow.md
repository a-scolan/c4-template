# Benchmark Agent Workflow

Single reference for the benchmark harness, agents, hooks, outputs, and trust rules.

Current protocol generation target is **`benchmark-v3`**.

## Entry points

- Human: workspace agent `Skill Benchmark Manager`
- Automation: `python test/scripts/skill_suite_tools.py self-test --iteration test/iteration-N --workspace-root .`

Stable public façades stay:

- `test/scripts/skill_suite_tools.py`
- `test/scripts/benchmark_access_hook.py`

Internal helpers now live under `test/scripts/benchmark/`. This refactor must remain iso-functional: same commands, same schemas, same hook behavior, same parallelism, same reporting contract.

## Required invariants

- Default trust boundary for `without_skill`: physical relocation of `.github/skills/` into `test/<iteration>/_disabled-skills/`
- Parallelism: allowed within a phase, forbidden across phase boundaries
- Default work unit: `<skill, eval_id, configuration, run_number>`
- `with_skill` starts only after skill restoration
- blind comparison starts only after `with_skill` completes
- `materialize-comparisons` must refresh `suite-summary.json` and `suite-summary.md` immediately
- Cross-iteration comparisons must support both numeric iterations (`iteration-N`) and named benchmark series (`<skill>-test`, `<skill>-test2`, `<skill>-test3`, ...)
- Never reuse an older `blind-comparisons.json` as fresh evidence
- Blind comparator workers must receive explicit evidence paths from `blind-compare-bundle` (A, B, grading spec). Do not rely on broad repository search during blind runs.
- Blind artifacts are run-scoped only: `.../blind/run-<N>/A.md|B.md` plus `blind-map.run-<N>.json` beside the eval directory. Legacy flat `blind/A.md`, `blind/B.md`, and `blind-map.json` are no longer generated.

If raw hook payloads omit `sessionId`, the wrapper must derive stable anonymous sessions per scope for stateful phases. If that derivation is ambiguous, reset hook state and serialize that phase as a safety fallback.

## Phase order

1. `clean-benchmark-artifacts` (skips git-tracked iteration directories)
2. `write-protocol-manifest`
3. `protocol-preflight`
4. relocate skills
5. run all `without_skill` workers in parallel waves
6. normalize + validate metrics
7. restore skills
8. run all `with_skill` workers in parallel waves
9. normalize + validate metrics
10. run blind comparison in parallel waves
11. `validate-executable-checks`
12. aggregate suite outputs
13. run an explicit Anthropic skill-authoring best-practices pass per benchmarked skill (inside each `synthesis.md`)

## Agent map

| Agent | Role |
| --- | --- |
| `skill-benchmark-manager` | Orchestrates phases, docs, exports, validation |
| `skill-benchmark-baseline` | Strict relocated `without_skill` worker |
| `skill-benchmark-baseline-hook-only` | Experimental hook-only baseline probe |
| `skill-benchmark-with-skill` | Targeted `with_skill` worker locked to one skill |
| `skill-blind-comparator` | Blind A/B judge |

Hard rule: workers set `agents: []`. No unconstrained subagent hops.
Hard rule: workers may write files only under `test/<iteration>/<skill>/`, scoped by the hook. No writes to scripts, hooks, or meta directories.

## Hook modes

Shared hook entrypoint: `test/scripts/benchmark_access_hook.py`

| Mode | Allowed scope |
| --- | --- |
| `benchmark_manager` | benchmark orchestration only; no MCP |
| `baseline` | `projects/shared/` only; narrow LikeC4 grounding only; writes under `test/<iteration>/<skill>/` |
| `baseline_hook_only` | same read scope as baseline, but skills remain present; probe only; writes under `test/<iteration>/<skill>/` |
| `with_skill_targeted` | locked target skill + `projects/shared/`; prompts from `evals/evals-public.json` only; writes under `test/<iteration>/<skill>/` |
| `blind_compare` | blinded `A.md` / `B.md` + target `grading-spec.json`; no MCP |

Narrow LikeC4 grounding is allowed only for scored answer-generation workers. Project listing, project summaries, and view browsing remain denied.

For robustness in skill-series iterations (for example `likec4-dsl-test4`), blind mode supports tightly scoped searches inside the active eval blind run directory (such as `.../blind/run-1/**`). Broad blind-phase search scopes remain denied.

## Worker write access

Worker agents (baseline, baseline_hook_only, with_skill_targeted) can write response files directly to disk under `test/<iteration>/<skill>/` paths. This avoids the overhead of the manager having to materialize worker text output. The hook enforces:

- Writes must be under `test/` and target a valid benchmark iteration directory
- Each worker session is locked to one iteration after its first allowed write; cross-iteration writes in the same session are denied
- Writes under `test/scripts/`, `test/_agent-hooks/`, and `test/_meta/` are denied
- Writes to `_`-prefixed skill directories (e.g. `_disabled-skills/`) are denied

The manager instructs each worker with the exact output file path (e.g. `test/<iteration>/<skill>/eval-<id>/<config>/run-<N>/response.md`). After a phase completes, the manager uses `summarize-phase` and `aggregate` to build summaries from the written files.

## Trace levels

Default agent setting is now `BENCH_TRACE_LEVEL=normal`, which means no trace file by default.

- `normal` / `off`: no hook trace artefact
- `audit`: keep only resolved decisions in `test/_agent-hooks/hook-audit.jsonl`
- `debug`: keep the raw debug log and the resolved audit log

Legacy compatibility remains: `BENCH_DEBUG_HOOKS=true` still maps to `debug`.

## Canonical outputs vs disposable outputs

Keep as canonical benchmark outputs:

- per-eval responses and blind artefacts under `test/<iteration>/<skill>/`
- `with_skill-summary.json`, `without_skill-summary.json`
- `with_skill-run-metrics.json`, `without_skill-run-metrics.json`
- `blind-comparisons.json`
- executable-check reports
- `_meta/protocol-lock.json`, metric validation/normalization summaries, optional caveats
- `suite-summary.json` and `suite-summary.md`

Treat as disposable generated artefacts:

- `test/_agent-hooks/`
- `test/_live-mcp-probe/`
- `test/scripts/__pycache__/`
- `test/<iteration>/<skill>/_skill-creator-review-workspace*/`
- `test/<iteration>/<skill>/skill-creator-review.html`
- `test/<iteration>/<skill>/skill-creator-benchmark.json`

The harness no longer generates `skill-creator-benchmark.md` or `export-summary.json`.

Use `python test/scripts/skill_suite_tools.py prune-generated-artifacts --iteration test/iteration-N --workspace-root .` to remove disposable per-iteration review exports after a run.

## Review/export flow

When a human review is needed:

1. `export-review-workspace`
2. `write-skill-creator-benchmark`
3. `write-static-review`

These outputs are derived from canonical JSON results and should normally be regenerated locally rather than committed.

## Anthropic skill-authoring best-practices pass (mandatory)

After suite summaries are regenerated, each benchmarked skill must receive a dedicated quality pass documented in `test/<iteration>/<skill>/synthesis.md`.

This pass must remain evidence-based and use benchmark artifacts (blind comparisons, summaries, executable checks, eval definitions), plus targeted inspection of the skill text. It should explicitly cover:

1. **Concision / token economy**: keep only high-value instructions; remove explanatory fluff Claude already knows.
2. **Degrees of freedom fit**: tune strictness to task fragility (high freedom for contextual tasks, low freedom for brittle sequences).
3. **Triggerability metadata quality**: verify `name` and `description` are specific about capability and trigger contexts.
4. **Progressive disclosure quality**: maintain focused core instructions and one-level references to detailed files.
5. **Workflow + feedback-loop quality**: ensure complex tasks have clear steps and validation/retry loops.
6. **Anti-pattern scan + concrete rewrites**: detect vague descriptions, option overload, stale guidance, and platform-path pitfalls; provide targeted edits.

The quality pass is considered incomplete if these checks are not explicitly addressed.

## Blind comparison robustness checklist

Before launching comparator workers for an eval:

1. Run `blind-compare-bundle` for that exact `<iteration, skill, eval_id, run_number>`.
2. Pass the returned `blind_artifacts.A`, `blind_artifacts.B`, and `eval_artifacts.grading_spec_path` directly in the delegation prompt.
3. If any of these files are missing, fail fast and repair artifacts before dispatching comparator workers.

## Diagnostics

- Use `validate-hook-audit` when trace level is `audit` or `debug`
- If audit JSONL is malformed, delete `test/_agent-hooks/` and rerun the affected phase
- Use `reset-hook-state` before forcing a serialized fallback for stateful modes

## Trust summary

- Baseline trust comes from physical relocation first, hooks second
- Hook-only baseline is diagnostic, not the default publication path
- One losing eval is a disagreement to verify, not an automatic skill failure
