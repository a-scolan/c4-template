# Benchmark Agent Workflow

Single reference for the benchmark harness, agents, hooks, outputs, and trust rules.

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
- Never reuse an older `blind-comparisons.json` as fresh evidence

If raw hook payloads omit `sessionId`, the wrapper must derive stable anonymous sessions per scope for stateful phases. If that derivation is ambiguous, reset hook state and serialize that phase as a safety fallback.

## Phase order

1. `clean-benchmark-artifacts`
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

## Agent map

| Agent | Role |
| --- | --- |
| `skill-benchmark-manager` | Orchestrates phases, docs, exports, validation |
| `skill-benchmark-baseline` | Strict relocated `without_skill` worker |
| `skill-benchmark-baseline-hook-only` | Experimental hook-only baseline probe |
| `skill-benchmark-with-skill` | Targeted `with_skill` worker locked to one skill |
| `skill-blind-comparator` | Blind A/B judge |

Hard rule: workers set `agents: []`. No unconstrained subagent hops.

## Hook modes

Shared hook entrypoint: `test/scripts/benchmark_access_hook.py`

| Mode | Allowed scope |
| --- | --- |
| `benchmark_manager` | benchmark orchestration only; no MCP |
| `baseline` | `projects/shared/` only; narrow LikeC4 grounding only |
| `baseline_hook_only` | same read scope as baseline, but skills remain present; probe only |
| `with_skill_targeted` | locked target skill + `projects/shared/`; prompts from `evals/evals-public.json` only |
| `blind_compare` | blinded `A.md` / `B.md` + target `grading-spec.json`; no MCP |

Narrow LikeC4 grounding is allowed only for scored answer-generation workers. Project listing, project summaries, and view browsing remain denied.

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

## Diagnostics

- Use `validate-hook-audit` when trace level is `audit` or `debug`
- If audit JSONL is malformed, delete `test/_agent-hooks/` and rerun the affected phase
- Use `reset-hook-state` before forcing a serialized fallback for stateful modes

## Trust summary

- Baseline trust comes from physical relocation first, hooks second
- Hook-only baseline is diagnostic, not the default publication path
- One losing eval is a disagreement to verify, not an automatic skill failure
