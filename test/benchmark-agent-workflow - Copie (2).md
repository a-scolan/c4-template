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
- `protocol-preflight` auto-resets hook state for all worker modes (`baseline`, `with_skill_targeted`, `blind_compare`) at iteration start — this is the mandatory safeguard against cross-iteration session contamination (anonymous session IDs are stable-prefix-derived and persist across runs)
- `disable-workspace-skills` is idempotent: if skills are already relocated and the manifest exists, a second call returns the existing manifest instead of raising an error
- `materialize-comparisons` must refresh `suite-summary.json` and `suite-summary.md` immediately
- `materialize-comparisons` must merge incrementally by `(eval_id, run_number)` (never overwrite previous comparisons) and refresh `suite-summary.json` + `suite-summary.md` immediately
- `materialize-comparisons-stdin` without `--raw-json` must persist each payload to a unique `_meta/raw-comparison-*.json` journal file (no shared overwrite target)
- `blind-compare-bundle` must provide a per-task `raw_output_path`, and comparator workers should journal their wrapped JSON there before returning so large blind judgments never depend on chat transport
- `resume-finalize` is the preferred recovery/finalization command after interruptions (auto-materialize missing blind outputs from `_meta`, run pre-check, then aggregate)
- Cross-iteration comparisons must support both numeric iterations (`iteration-N`) and named benchmark series (`<skill>-test`, `<skill>-test2`, `<skill>-test3`, ...)
- Never reuse an older `blind-comparisons.json` as fresh evidence
- Blind comparator workers must receive explicit evidence paths from `blind-compare-bundle` (A, B, grading spec). Do not rely on broad repository search during blind runs.
- Blind artifacts are run-scoped only: `.../blind/run-<N>/A.md|B.md` plus `blind-map.run-<N>.json` beside the eval directory. Legacy flat `blind/A.md`, `blind/B.md`, and `blind-map.json` are no longer generated.
- Hook path enforcement must derive access scope only from explicit path-bearing tool fields (for example `filePath`, `path`, `includePattern`, `uri`) and must not infer file access from free-text prompt/editor context.
- `snapshot-public-evals` now materializes worker-local public prompt inputs at `test/<iteration>/<skill>/eval-<id>/input/prompt.md` and `prompt.json`; baseline workers may read only these prompt files (plus their own benchmark artefacts), not project folders.
- `snapshot-public-evals` is relocation-aware: if `.github/skills/` is temporarily empty during strict baseline, it falls back to `test/<iteration>/_disabled-skills/` so prompt snapshots can still be generated without a manual restore/disable bounce.
- `with_skill_targeted` workers may read the same iteration-local prompt input files (`test/<iteration>/<skill>/eval-<id>/input/prompt.md|prompt.json`) in addition to `evals/evals-public.json`, while `grading-spec.json` remains hidden.
- Benchmark-manager command guardrails now fail fast for missing required subcommand flags (for example `summarize-config` without `--config`) to prevent partial/manual reruns.
- Benchmark-manager command parsing now accepts safe `for ... do ... done` batching only when every command inside the loop body is still on the allowlist.

If raw hook payloads omit `sessionId`, the wrapper must derive stable anonymous sessions per scope for stateful phases. If that derivation is ambiguous, reset hook state and serialize that phase as a safety fallback.

**Cross-iteration contamination rule:** Anonymous session IDs are derived from a stable prefix (e.g. `anonymous-with_skill_targeted-likec4-dsl`). A session locked to iteration N will deny writes to iteration N+1. `protocol-preflight` now resets all worker modes automatically. Never skip it when starting a new iteration, even for a re-run.

## Eval and grading calibration

- Revalidate domain-specific truth-claims against authoritative docs or bundled workspace references before changing prompts, expected outputs, or expectations.
- Prefer contrastive prompts when the failure mode is a near miss (for example inherited scope vs redeclared scope, chained dynamic steps vs standalone arrows, cumulative deployment tags vs replacement semantics, relationship kind matching, or repeated `--file` validation filters).
- `grading-spec.json` may include optional comparator-only guidance fields (for example `grading_guidance`) to capture decisive tie-break rules without leaking them into public prompts.
- `grading-spec.json` may include optional grader-only execution metadata at two levels: top-level `default_execution_checks` (skill-level defaults) and eval-level `execution_checks`. Effective checks are merged per eval (eval entries override same-name defaults) and must remain optional so non-executable evals still fit the same framework.
- Persist benchmark policy changes in local maintained surfaces (`.github/agents/*.agent.md`, `test/scripts/skill_suite_tools.py`, this workflow doc). Do not rely on local edits under `.github/skills/skill-creator/` for long-term contract ownership.
- When an eval asks for an exact command or exact DSL snippet, unsupported nearby alternatives should count as incorrect content, not as a stylistic variant.
- Do not oversimplify scoped `include *` semantics in scoped views to “only the local subtree”: the scoped element and its direct children are the base include, but neighboring elements and derived relationships may also become visible because of those included elements.

## Phase order

1. `clean-benchmark-artifacts` (skips git-tracked iteration directories)
2. `write-protocol-manifest`
3. `protocol-preflight` — **automatically resets hook state for `baseline`, `with_skill_targeted`, and `blind_compare` modes** (prevents cross-iteration scope contamination from previous iteration sessions)
4. relocate skills
5. run all `without_skill` workers in parallel waves
6. `write-run-metrics` (or `write-run-metrics-auto`) for each `<config, run_number>` to the **per-run path** `_runs/<config>/run-<N>-metrics.json` (never directly to `<config>-run-metrics.json`)
7. normalize + validate metrics
8. restore skills
9. run all `with_skill` workers in parallel waves
10. `write-run-metrics` (or `write-run-metrics-auto`) for each `<config, run_number>` to the same per-run path pattern
11. normalize + validate metrics
12. `reset-blind-comparisons` for each skill (required before `prepare-blind` on a re-run or fresh run)
13. run blind comparison in parallel waves
14. `validate-executable-checks`
15. `resume-finalize` (or `pre-aggregate-check` + `aggregate` when manual control is needed); fail if blind coverage is incomplete for prepared eval/run pairs
16. run an explicit Anthropic skill-authoring best-practices pass per benchmarked skill (inside each `synthesis.md`)

## Agent map

| Agent | Role |
| --- | --- |
| `skill-benchmark-manager` | Orchestrates phases, docs, exports, validation |
| `skill-benchmark-baseline` | Strict relocated `without_skill` worker |
| `skill-benchmark-baseline-hook-only` | Experimental hook-only baseline probe |
| `skill-benchmark-with-skill` | Targeted `with_skill` worker locked to one skill |
| `skill-blind-comparator` | Blind A/B judge |

Hard rule: workers set `agents: []`. No unconstrained subagent hops.
Hard rule: answer-generation workers may write only under `test/<iteration>/<skill>/`, scoped by the hook. Blind comparator workers are the sole exception: they may also write a single explicit raw journal file under `test/<iteration>/_meta/raw-comparison-*.json`.

## Hook modes

Shared hook entrypoint: `test/scripts/benchmark_access_hook.py`

| Mode | Allowed scope |
| --- | --- |
| `benchmark_manager` | benchmark orchestration only; no MCP |
| `baseline` | no project-folder reads; worker prompt inputs under `test/<iteration>/<skill>/eval-*/input/` + narrow LikeC4 grounding only; writes under `test/<iteration>/<skill>/` |
| `baseline_hook_only` | same read scope as baseline, but skills remain present; probe only; writes under `test/<iteration>/<skill>/` |
| `with_skill_targeted` | locked target skill only; prompts from `test/<iteration>/<skill>/eval-*/input/prompt.md|prompt.json` or `evals/evals-public.json`; writes under `test/<iteration>/<skill>/` |
| `blind_compare` | blinded `A.md` / `B.md` + target `grading-spec.json`; no MCP |

Narrow LikeC4 grounding is allowed only for scored answer-generation workers. Project listing, project summaries, and view browsing remain denied.

For robustness in skill-series iterations (for example `<skill>-test4`), blind mode supports tightly scoped searches inside the active eval blind run directory (such as `.../blind/run-1/**`). Broad blind-phase search scopes remain denied.

## Worker write access

Worker agents (baseline, baseline_hook_only, with_skill_targeted) can write response files directly to disk under `test/<iteration>/<skill>/` paths. This avoids the overhead of the manager having to materialize worker text output. The hook enforces:

- Writes must be under `test/` and target a valid benchmark iteration directory
- Each worker session is locked to one iteration after its first allowed write; cross-iteration writes in the same session are denied
- Writes under `test/scripts/`, `test/_agent-hooks/`, and `test/_meta/` are denied
- Writes to `_`-prefixed skill directories (e.g. `_disabled-skills/`) are denied

The manager instructs each worker with the exact output file path (e.g. `test/<iteration>/<skill>/eval-<id>/<config>/run-<N>/response.md`). After a phase completes, the manager uses `write-run-metrics`, `summarize-phase` and `aggregate` to build metrics and summaries from the written files.

For strict baseline and hook-only baseline runs, prefer worker-local prompt inputs over `_meta` snapshots: read prompts from `test/<iteration>/<skill>/eval-<id>/input/prompt.md` (or `prompt.json`). `_meta` prompt snapshots remain a manager artifact.

For `with_skill` runs, you can also use these iteration-local prompt inputs. This avoids hook denials when a worker flow uses prompt files produced by `snapshot-public-evals` instead of reopening skill files.

When calling `write-run-metrics` (manual timestamps) or `write-run-metrics-auto` (derive timing from `response.md` mtimes) after workers complete, write to the **per-run path** `test/<iteration>/<skill>/_runs/<config>/run-<N>-metrics.json` (not directly to `<skill>/<config>-run-metrics.json`). `summarize-phase` automatically detects per-run files under `_runs/<config>/`, calls `refresh_run_metrics_collection` to consolidate them into the canonical `<config>-run-metrics.json` (with a `runs[]` array), then builds the summary. Writing directly to the consolidated path bypasses this and produces a flat object that fails `pre-aggregate-check`.

Blind comparator workers remain read-mostly, but may additionally journal one wrapped raw payload per task under the exact `raw_output_path` returned by `blind-compare-bundle` (for example `test/<iteration>/_meta/raw-comparison-<skill>-eval-<id>-run-<n>.json`). That keeps large comparator reasoning out of chat transport while preserving an auditable per-task journal.

## Metrics corruption prevention

Workers must write **one JSON object per file**, not append. If a worker batch-processes multiple evals in one session and writes metrics sequentially, always use `create_file` (or an atomic overwrite with `replace_string_in_file`) per metrics file — never open-and-append. Multiple JSON objects in the same `eval-N-metrics.json` file cause `"Extra data"` JSON parse errors that break `summarize-phase`.

Recovery path when per-eval metrics are corrupted: use `write-run-metrics --config <config> --run-number <N> ...` (explicit values) or `write-run-metrics-auto --iteration <...> --skill <...> --config <...> --run-number <N>` (filesystem-derived timing) to overwrite each corrupted file individually via the manager CLI (the manager is the only role allowed to repair metrics files across configurations). Do NOT use worker subagents to repair `_runs/without_skill/` files from a `with_skill_targeted` session — the hook scope mismatch will cause denial errors.

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
2. Pass the returned `blind_artifacts.A`, `blind_artifacts.B`, `eval_artifacts.grading_spec_path`, and `raw_output_path` directly in the delegation prompt.
3. **`raw_output_path` is a write-only destination.** Never include it as a read target and never instruct the comparator to read or verify it. It is a journal path for the comparator's output. Attempting to read it triggers a hook denial that does NOT mean A.md or B.md are blocked.
4. Materialize from that `raw_output_path` immediately after the worker acknowledges it wrote the file.
5. If any of the blind artifact files (A.md, B.md, grading-spec) are missing, fail fast and repair artifacts before dispatching comparator workers.

## Diagnostics

- Use `validate-hook-audit` when trace level is `audit` or `debug`
- If audit JSONL is malformed, delete `test/_agent-hooks/` and rerun the affected phase
- Use `reset-hook-state` before forcing a serialized fallback for stateful modes

## Trust summary

- Baseline trust comes from physical relocation first, hooks second
- Hook-only baseline is diagnostic, not the default publication path
- One losing eval is a disagreement to verify, not an automatic skill failure
