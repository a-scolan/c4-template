# Critical Synthesis — `likec4-dsl` Benchmark

**Iteration:** `likec4-dsl-test5`
**Protocol:** benchmark-v3
**Evals:** 29 (ids 0-28), 2 run(s) per configuration
**Generated:** 2026-03-30

---

## 1. Quantitative results

| Metric | `with_skill` | `without_skill` | Δ |
|---|---|---|---|
| **Blind win rate** | **44/58 = 75.86%** | 5/58 = 8.62% | +67.24 pp |
| **Expectation pass rate** | **0.9724** | 0.7638 | **+0.2086** |
| **Rubric score (0–10)** | **9.2586** | 7.4138 | **+1.8448** |
| Seconds / eval | 0.0 s | 0.1034 s | -0.1034 |
| Words / eval | 53.8276 | 236.2414 | -182.4138 |
| Files read | 29.0 | 29.0 | 0.0 |
| Executable validity | 0.6667 | 0.5818 | +0.0849 |

Overall signal is **strongly positive** for `with_skill`: higher quality and expectation coverage, with higher executable validity and substantially shorter outputs.

---

## 2. Eval-by-eval analysis

| Eval | Topic | Winner | Exp with | Exp without | Key discriminator |
|---|---|---|---|---|---|
| 0 | validate command + JSON fields | with_skill | high | low | exact CLI + filtered fields interpretation |
| 1 | config include + nearest config scope | with_skill | high | med | correct `include.paths` + scope rule |
| 2 | export png flags | with_skill | high | med | strict CLI shape and options |
| 3 | dynamic sequence basics | with_skill | high | low | required `dynamic view` + sequence variant |
| 4 | view-local style targeting | with_skill | high | high | cleaner minimal snippet |
| 5 | named deployment instances | with_skill | high | high | stricter minimal named-instance form |
| 6 | `_` vs `*` vs `**` predicate | mixed | med | med | semantics unstable between runs |
| 7 | extends scope inheritance | with_skill | high | high | cleaner inheritance explanation |
| 8 | predicateGroup reuse form | with_skill | high | med | exact reusable mechanism syntax |
| 9 | chained + parallel dynamic | with_skill/tie | high | high | mostly tie, slight structure edge |
| 10 | cumulative deployment tags fixture | with_skill | high | med | single minimal fixture compliance |
| 11 | metadata merge semantics | with_skill | high | med | correct array merge behavior |
| 12 | deployment styling limits | with_skill/tie | high | high | both correct, minor concision edge |
| 13 | tag/property ordering fix | with_skill | high | low | exact invalidity cause + minimal fix |
| 14 | invalid `styles` top-level | with_skill | high | med | better allowed-top-level correction |
| 15 | identifier validity set | with_skill | high | med | correct `payment-api` handling |
| 16 | invalid parent-child relationship | with_skill | high | high | stricter explicit correction form |
| 17 | cross-file FQN resolution | mixed | high | high | both good, style-level variance |
| 18 | relationship kind disambiguation | mixed | high | high | both good, minor structure variance |
| 19 | scoped `include *` semantics | with_skill | high | med | direct-children semantics precision |
| 20 | 2-file targeted validate | with_skill | high | low | strict repeated `--file` shape |
| 21 | child view scope inheritance | with_skill/tie | high | high | mostly tie, cleaner final form |
| 22 | chained dynamic strictness | tie/without | high | high | very narrow margin, format preference |
| 23 | cumulative tag filters | tie | high | high | equivalent correctness |
| 24 | async matcher exactness | with_skill | high | med | metadata block + exact matcher |
| 25 | 3-file validate + filteredFiles=2 meaning | mixed | med | med | one run flipped on command strictness |
| 26 | exact global predicate reuse | with_skill/tie | high | high | mostly equivalent |
| 27 | scoped `*` direct-children choice | with_skill | high | med | incoming-only snippet precision |
| 28 | unkinded extend is wrong | tie | high | high | equivalent exactness |

### Observations

- Biggest wins are on **strict CLI and strict DSL syntax** evals (0, 1, 2, 20).
- High-variance spots are mostly **near-ties** where both outputs are technically correct but differ in concision/formatting (9, 12, 21, 23, 26, 28).
- Real disagreement zones to verify later: **6, 17, 18, 22, 25** (winner flips or narrow margins).

---

## 3. Executable validity analysis

Executable validity improved from **0.5818 → 0.6667** (+0.0849), which is directionally good but still below 0.8. This is consistent with a skill that wins on semantic guidance but still emits occasional snippet-shape drift under strict checks. Metric is **reliable enough** here because delta direction matches blind/expectation gains.

---

## 4. Skill design assessment

### Strengths

1. Strong control of exact LikeC4 CLI forms and JSON-field interpretation.
2. Better precision on contrastive DSL semantics (`extend` identity matching, scoped include behavior).
3. Better adherence to minimal, runnable snippets under strict prompts.
4. Consistently better expectation coverage on syntax-sensitive tasks.

### Weak areas

1. Predicate edge semantics variance (`_` vs `**`) on eval 6.
2. Some mixed outcomes on “both-correct” prompts where concision/style decides winner (17, 18, 22, 25).
3. Executable validity still moderate; a subset of snippets remains fragile.
4. Occasional over-verbose alternatives in answer bodies can weaken strictness.

---

## 5. Priority recommendations

**P1 — Critical (direct impact on baseline failures)**
- Add explicit “never substitute command families/flags” guardrails for validate/export eval types.
- Add one hard rule card for scoped predicates (`*`, `_`, `**`) with one-line truth table.

**P2 — Important (improved precision)**
- Tighten output contract for strict prompts: “single final snippet, no alternative variants unless asked”.
- Add anti-ambiguity pattern for relationship extension matchers with kind/title/source/target.

**P3 — Nice to have (robustness)**
- Add 2-3 extra discriminative evals for near-tie clusters (22/23/28).
- Add lightweight snippet self-check checklist before final answer emission.

---

## 6. Anthropic skill-authoring best-practices pass

- **Concision / token economy:** remove redundant alternative snippets when prompt asks for one exact output.
- **Degrees of freedom fit:** keep low freedom on strict syntax/CLI tasks; allow moderate freedom on explanation-only tasks.
- **Triggerability metadata quality:** current trigger quality is strong for LikeC4 DSL/CLI requests; keep wording explicit on “exact syntax/flags”.
- **Progressive disclosure quality:** maintain short core rules + one-level references (no deep nesting needed).
- **Workflow + feedback-loop quality:** keep a compact generate→self-check→finalize loop for strict commands/snippets.
- **Anti-pattern scan + rewrites:** avoid stale flag aliases and ambiguous “equivalent command” statements when eval expects exact form.

---

## 7. Verdict

`likec4-dsl` is **effective** in this iteration: it clearly outperforms baseline on blind wins, expectation pass rate, and rubric score. Caveat: several evals are high-variance near-ties, so one more discriminative pass is recommended before treating those disagreements as settled.

## Errors to fix later (benchmark process)

1. Manager invocation mistake: `summarize-config` initially called without required `--config`.
2. Phase-state mismatch: snapshot attempted while skills were relocated; required restore then strict re-disable.
3. `with_skill` read-scope mismatch on evals 20–24 run-1 (prompt source path denied) required targeted rerun.
4. Benchmark-manager allowlist friction on broad shell patterns/loops made bundle/materialization steps slower and more manual.
5. Metrics timestamps were minimal placeholders; if needed, capture real start/finish per run for stronger timing fidelity.
