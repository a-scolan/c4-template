# Critical Synthesis — `likec4-dsl` Benchmark

**Iteration:** `likec4-dsl-test6`
**Protocol:** benchmark-v3
**Evals:** 32 (ids 0-31), 2 run(s) per configuration
**Generated:** 2026-03-30

---

## 1. Quantitative results

| Metric | `with_skill` | `without_skill` | Δ |
|---|---|---|---|
| **Blind win rate** | **50/64 = 78.1%** | 7/64 = 10.9% | +67.2 pp |
| **Expectation pass rate** | **0.9661** | 0.7369 | **+0.2292** |
| **Rubric score (0–10)** | **9.4406** | 7.1656 | **+2.2750** |
| Seconds / eval | 1.7388 s | 1.5990 s | +0.1398 s |
| Words / eval | 55.8125 | 65.2500 | -9.4375 |
| Files read | 32.0 | 32.0 | +0.0 |
| Executable validity | 0.6042 | 0.6667 | -0.0625 |

Strong positive quality signal overall (wins, expectations, rubric), with a small speed regression and a notable executable-validity drop that must be interpreted carefully (see section 3).

---

## 2. Eval-by-eval analysis

| Eval | Topic | Winner | Exp with | Exp without | Key discriminator |
|---|---|---|---|---|---|
| **0** | validate command flags | with_skill | 4-5/5 | 0/5 | Exact `validate --json --no-layout --file` form + filtered counters |
| **1** | config include + nearest config | with_skill | 5/5 | 2/5 | Exact `include.paths` + nearest-config explanation |
| **3** | dynamic sequence arrows | with_skill | 5/5 | 2-3/5 | Correct `dynamic view` + sequence return-arrow form |
| **4** | scoped styling location | mixed/tie | 5/5 | 5/5 | Both often correct; discriminator mainly concision |
| **8** | predicateGroup syntax | mixed | 5/5 | 4-5/5 | Exact reusable-predicate block vs near-miss syntax |
| **10** | deployment cumulative tags fixture | mixed | 5/5 | 3-4/5 | Explicit `instanceOf` fixture quality |
| **11** | metadata merge vs overwrite | mixed | 3-5/5 | 3-5/5 | Correct semantic claim on merge array behavior |
| **12** | deployment styling limits | with_skill | high | lower | Correct rejection of unsupported constructs |
| **18/24/28/31** | relationship identity matcher | with_skill | high | lower | Precise matching on source/target/title/**kind** |
| **27** | scoped `include *` semantics | with_skill | high | lower | Correct “direct children base set + neighbors via relations” |

### Observations

The biggest wins come from contrastive DSL traps (exact command forms, relationship-kind matching, scoped predicates). Most weak discriminators are already-correct baseline cases (style location, some deployment snippets). Variance is high on several syntax-near evals, indicating prompt sensitivity more than capability collapse.

---

## 3. Executable validity analysis

This is the main paradox: quality metrics improve strongly while executable validity drops by 6.25 points. The likely reason is output format preference (helpful prose around snippets, shell examples, or mixed snippets) rather than DSL understanding loss. For this skill, executable validity is useful but should be weighted with caution against blind/rubric evidence.

---

## 4. Skill design assessment

### Strengths

- Enforces exact CLI/DSL forms for brittle tasks.
- Improves disambiguation where near-miss syntax exists.
- Better at explaining semantic traps (scope inheritance, relationship identity).
- Produces shorter responses with better benchmark quality.

### Weak areas

- Some variance remains on close semantic pairs (e.g., reusable predicate and deployment fixtures).
- Occasional over-formatting hurts executable checks.
- A few ties suggest evals that are now under-discriminating.
- Some references in worker flow were missing/nonexistent, indicating fragility in ancillary guidance.

---

## 5. Priority recommendations

**P1 — Critical (direct impact on baseline failures)**
- Add stricter in-skill “exact syntax guardrails” for deployment and relationship-extension matchers.
- Add one explicit “final self-check” step: verify required keyword/flag tokens are present before final answer.

**P2 — Important (improved precision)**
- Add short canonical snippets for high-variance eval families (predicateGroup, deployment fixture, scoped include semantics).
- Reduce ambiguity in instructions for return-arrow and parallel-block forms.

**P3 — Nice to have (robustness)**
- Add adversarial evals separating “almost right” from exact syntax.
- Add execution-oriented checks that penalize prose-only answers when snippet-first is required.

---

## 6. Anthropic skill-authoring best-practices pass

- **Concision / token economy:** Keep only high-signal syntax traps; trim explanatory duplicates.
- **Degrees of freedom fit:** Keep strictness for command/snippet evals; allow lighter prose freedom in explanation-only prompts.
- **Triggerability metadata quality:** `likec4-dsl` trigger remains good for syntax/CLI asks; could mention “exact command/snippet” cues more explicitly.
- **Progressive disclosure quality:** Good overall; ensure references used by workers actually exist and are stable.
- **Workflow + feedback-loop quality:** Add explicit verify-before-final step for required flags/keywords.
- **Anti-pattern scan + rewrites:** Avoid stale/nonexistent reference pointers; reduce option overload by grouping “required vs optional” syntax forms.

---

## 7. Verdict

The skill is effective in this campaign: strong blind wins, higher expectation pass rate, and higher rubric scores across 64 comparisons. Main caveat: executable validity regressed, likely due to formatting behavior rather than core DSL knowledge. Next iteration should focus on snippet-first discipline and reducing high-variance near-miss cases.