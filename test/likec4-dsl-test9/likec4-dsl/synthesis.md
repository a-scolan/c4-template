# Skill Synthesis — `likec4-dsl` | Iteration: likec4-dsl-test9

Generated: 2026-03-31 | Runs: 2 per eval | Evals: 32

---

## 1. Quantitative summary

| Metric | With skill | Without skill | Δ |
|---|---|---|---|
| Blind win rate | 81.3% (52 wins) | 9.4% (6 wins) | +71.9 pp |
| Ties | 6 (9.4%) | — | — |
| Expectation pass rate | 0.982 | 0.704 | **+0.279** |
| Rubric score (0–10) | 9.51 | 6.83 | **+2.68** |
| Seconds / eval | 27.70 s | 32.45 s | **−4.76 s** |
| Words / eval | 77.0 | 90.0 | **−13.0** |
| Files read / eval | 32.0 | 32.0 | 0 |
| Executable validity | 88.1% | 87.8% | **+0.3 pp** |

**Verdict: strong positive signal.** The skill wins most blind comparisons, improves expectation and rubric outcomes substantially, and is still shorter and faster than baseline. Executable validity is only marginally better, so the main gains are quality and precision rather than checker-facing behavior.

---

## 2. Per-eval breakdown (blind comparison outcomes)

| Eval | Outcomes | Flips? | Topic | Key discriminator |
|---|---|---|---|---|
| 0 | with_skill | no | File-scoped validate | Exact `validate --json --no-layout --file` semantics and filtered-field interpretation |
| 1 | with_skill | no | Minimal config JSON | Correct `$schema` + `name` + `include.paths` and nearest-config scope |
| 2 | with_skill | no | PNG export command | Better `export png` filter/project-path alignment |
| 3 | with_skill | no | Dynamic sequence view | `variant sequence` + backward `<-` response arrows |
| 4 | TIE / with_skill | yes | View-local styling | Small selector-syntax / minimal-wrapper difference only |
| 5 | with_skill | no | Named deployment instances | Exact `deployment` + VM + `instanceOf` pattern |
| 6 | with_skill | no | `_`, `*`, `**` predicates | `**` must stay relationship-qualified, not plain recursive descendants |
| 7 | with_skill | no | Inherited scope via `extends` | Exact inherited-scope and inbound predicate form |
| 8 | with_skill | no | Reusable predicate groups | Canonical `global { predicateGroup ... }` syntax won |
| 9 | with_skill | no | Chained dynamic hop | Correct single `parallel { ... }` block and hop-local body |
| 10 | with_skill | no | Cumulative deployment-tag fixture | More exact self-contained deployment fixture |
| 11 | with_skill | no | `extend` metadata merge | Correct duplicate metadata merge-into-array semantics |
| 12 | with_skill / without_skill | yes | Deployment-view limitations | Unsupported `include * with {}` / `global style` handling remains borderline |
| 13 | with_skill | no | Body tag ordering | `#tag` before property inside the element body |
| 14 | with_skill | no | Invalid top-level `styles` | Correct allowed top-level block list and repair |
| 15 | with_skill | no | Identifier validity | Exact valid/invalid identifier classification mattered |
| 16 | with_skill | no | Parent-child relationship misuse | Better explicit diagnosis of invalid parent→child relationship |
| 17 | without_skill | no | Cross-file FQN resolution | Baseline stayed slightly crisper on lexical-scope rewrite |
| 18 | with_skill | no | Async relationship extend identity | Kind/title disambiguation stayed consistently stronger |
| 19 | with_skill | no | Scoped `include *` semantics | Better direct-children base set and predicate anchoring |
| 20 | with_skill | no | Multi-file validate CLI | Exact repeated `--file` invariants and filtered counters |
| 21 | with_skill | no | Valid inherited-scope view | Skill won overall despite one baseline isolation-failure artifact |
| 22 | without_skill | no | Chained dynamic continuation | Minimal wrapper preference still favors baseline here |
| 23 | TIE | no | Deployment tag inheritance | Both answers were stably equivalent |
| 24 | with_skill | no | Async matcher correction | Metadata-bearing `extend` block decided the eval |
| 25 | with_skill | no | `filteredFiles = 2` interpretation | Exact tri-file validate command shape mattered |
| 26 | with_skill | no | PredicateGroup precision | Exact `where kind is service` / `where tag is #deprecated` syntax |
| 27 | with_skill | no | Scoped incoming relationships | Correct incoming predicate form around `cloud.backend` |
| 28 | TIE / without_skill | yes | Exact unkinded-extend rejection | Very small wording differences around ambiguity vs wrong-target risk |
| 29 | with_skill | no | Multiple-choice chained-step answer | More precise one-sentence elimination of non-A options |
| 30 | TIE | no | Exact tag filter matrix | Both answers were stably exact |
| 31 | with_skill | no | Matcher classification triage | Correctly marking option (3) as wrong, not ambiguous |

**Disagreements to verify:** 4, 12, 28. These are the only true blind winner-flip pockets and are better treated as benchmark-hardening candidates than immediate skill regressions.

---

## 3. Executable validity detail

| Config | Applicable runs | Valid rate |
|---|---|---|
| with_skill | 42 | 88.1% |
| without_skill | 41 | 87.8% |

Δ = **+0.3 pp** in favor of the skill.

Takeaway: executable validity is nearly neutral this round. The skill does not meaningfully hurt checker validity, but checker-passing behavior is not the main source of the observed benchmark gains.

---

## 4. High-variance eval analysis

21 of 32 evals were flagged high-variance overall, but only **three** show true blind winner instability: **4, 12, 28**.

Most important patterns:

- **Stable strong wins**: exact CLI / exact DSL-shape tasks remain reliable wins (`0`, `1`, `5`, `11`, `14`, `20`, `24`, `25`, `31`).
- **Stable weak spots**: `17` (cross-file FQN explanation precision) and `22` (minimal chained-dynamic continuation form) are the clearest persistent losses.
- **Near-ties / ambiguity pockets**: `4`, `12`, and `28` are close enough that wording and snippet minimalism still move the verdict.
- **Neutral islands**: `23` and `30` were stable ties, so they are not productive improvement targets right now.

The main conclusion is pleasantly boring: most of the skill’s gains are stable, and the instability is concentrated in a small, reviewable subset rather than spread across the suite.

---

## 5. Comparison with previous iteration (likec4-dsl-test8)

| Metric | test8 | test9 | Δ |
|---|---|---|---|
| Win rate | 76.6% | 81.3% | **+4.7 pp** |
| Expectation Δ | 0.214 | 0.279 | **+0.065** |
| Rubric Δ | 2.13 | 2.68 | **+0.55** |
| Time Δ / eval | **−6.60 s** | **−4.76 s** | +1.84 s |
| Executable Δ | +6.6 pp | +0.3 pp | −6.3 pp |

Headline read: benchmark quality improved over `likec4-dsl-test8` on the core blind and rubric metrics, while still keeping the skill faster than baseline. The only real softening versus the prior run is that executable-validity advantage largely flattened out.

---

## 6. Errors and issues for future benchmark improvements

1. **Baseline parallel dispatch hit a global subagent rate limit**  
   Baseline `run-2` for evals `17..31` needed targeted retries. This did not cause phase contamination, but it is a throughput / orchestration quality issue.

2. **Initial manager matrix omitted `eval-0`**  
   The miss was caught by `summarize-phase`, then repaired cleanly. This is exactly the kind of boring off-by-one that benchmarks should automate away forever.

3. **One baseline response surfaced a false-looking isolation failure**  
   `without_skill` eval `21`, run `2`, returned an isolation-failure message instead of task content. The overall protocol still validated, but this is a benchmark-quality signal worth investigating.

4. **Blind-isolation / aggregation health was otherwise clean**  
   Pre-aggregate checks passed, harness noise was clean, and there is no evidence of cross-phase or cross-run contamination in the final artifacts.

---

## 7. Skill improvement recommendations (Anthropic best-practices pass)

| Check | Finding |
|---|---|
| Concision / token economy | Good. The skill is **shorter** than baseline by 13.0 words/eval while still winning strongly. |
| Degrees of freedom fit | Mostly good, but still a bit loose on borderline syntax-choice evals (`12`, `17`, `22`, `28`). |
| Triggerability metadata | Looks healthy in practice: no extra file-read cost and no sign of under-triggering. |
| Progressive disclosure | Strong. The skill helps exact DSL/CLI questions without causing answer bloat. |
| Workflow + feedback loop | Strong on command-first and exact-snippet tasks (`0`, `20`, `24`, `25`, `31`). |
| Anti-pattern scan | Keep reinforcing unsupported deployment-view constructs, exact FQN repair across files, and matcher disambiguation when typed alternatives coexist. |

Concrete rewrites worth considering:

- Add one tiny **deployment-view unsupported syntax** reminder covering `include * with {}` and `global style`.
- Add one short **cross-file FQN** reminder that nested relative names do not survive file boundaries.
- Add one compact **typed matcher disambiguation** example showing when omitted kind is merely ambiguous vs simply wrong.
- Preserve the current concise style; the benchmark says brevity is helping, not hurting.
