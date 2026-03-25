# Critical Synthesis — `likec4-dsl` Benchmark

**Iteration:** `likec4-dsl-test3`  
**Protocol:** benchmark-v2  
**Evals:** 21 (ids 0–20), 1 run per configuration  
**Generated:** 2026-03-25

---

## 1. Quantitative results

| Metric | `with_skill` | `without_skill` | Δ |
|---|---|---|---|
| **Blind win rate** | **1/21 = 4.76%** | 0/21 = 0.00% | +4.76 pp |
| **Expectation pass rate** | **0.0476 (4.76%)** | 0.0000 (0.00%) | **+0.0476** |
| **Rubric score (0–10)** | **0.4381** | 0.1429 | **+0.2952** |
| Seconds / eval | 16.2381 s | 10.9048 s | +5.3333 s |
| Words / eval | 68.2857 | 66.9524 | +1.3333 |
| Files read | 21.0 | 0.0 | +21.0 |
| Executable validity | 0.6250 | 0.5333 | +0.0917 |

Overall signal: **methodologically weak and caveated**. The numeric deltas are positive for `with_skill`, but almost all blind comparisons are technical ties driven by blind-worker file-access failures rather than true A/B quality discrimination.

---

## 2. Eval-by-eval analysis

| Eval | Topic | Winner | Exp with | Exp without | Key discriminator |
|---|---|---|---|---|---|
| 0 | targeted validate command | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 1 | config include paths | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 2 | export png flags | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 3 | dynamic sequence syntax | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 4 | view-level styling scope | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 5 | deployment instances | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 6 | scoped predicate semantics | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 7 | extends + scope inheritance | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 8 | global predicateGroup reuse | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 9 | chained + parallel dynamic | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 10 | deployment tag inheritance | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 11 | extend metadata merge | TIE (low) | 0/5 | 0/5 | blind evidence inaccessible |
| 12 | deployment view limits | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 13 | tag/property ordering | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 14 | invalid top-level styles | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 15 | identifier validity rules | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 16 | parent-child relationship invalidity | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 17 | cross-file FQN resolution | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 18 | relationship extend matching | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 19 | scoped `*` semantics | TIE (low) | 0/0 | 0/0 | blind evidence inaccessible |
| 20 | two-file validate command | with_skill (high) | 5/5 | 0/5 | exact CLI + filteredFiles/filteredErrors interpretation |

### Observations

- The only discriminating eval is **20**, where `with_skill` clearly outperforms baseline.
- Evals **0–19** are non-discriminating in this run due to comparator sandbox access failures, not because outputs are equivalent.
- Therefore, this iteration should be treated as an **execution-quality probe**, not a decisive quality verdict on skill content.

---

## 3. Executable validity analysis

Executable validity improved from **0.5333** to **0.6250** (+0.0917) for `with_skill`. This indicates slightly better syntactic/semantic DSL shape in generated snippets. However, because blind comparison evidence was mostly unavailable, executable-validity uplift cannot be cleanly correlated with blind quality wins in this iteration.

Conclusion: executable validity is directionally positive but **insufficient alone** as a replacement for valid blind A/B access.

---

## 4. Skill design assessment

### Strengths
- Strong command-shape guidance for strict CLI tasks (shown on eval 20).
- Better adherence to expected JSON verification fields (`filteredFiles`, `filteredErrors`) when the task is explicit.
- Slightly better executable DSL validity rate than baseline.

### Weak areas
- Blind evaluation could not inspect most outputs, so skill impact is under-observed in this run.
- Current benchmark execution path is fragile to comparator file-access restrictions.
- Lack of discriminative blind evidence for 20/21 evals prevents robust skill diagnosis.

---

## 5. Priority recommendations

**P1 — Critical**
- Fix blind comparator bundle access so A/B artifacts are consistently readable for every eval.
- Re-run the same 21 eval matrix after access fix to obtain a trustworthy discriminative score.

**P2 — Important**
- Add a campaign guard that aborts/fails the run if comparator evidence access is denied for more than a small threshold (e.g., >10%).
- Capture explicit per-eval comparator health metadata to separate “true tie” from “blocked tie.”

**P3 — Nice to have**
- Add a second run (`run-2`) to quantify variance once blind access is stable.
- Expand executable checks with stricter semantic checks per eval intent.

---

## 6. Previous-run comparison (`likec4-dsl-test2` → `likec4-dsl-test3`)

Key deltas vs previous run:
- Blind win rate: **95.24% → 4.76%** (−90.48 pp)
- Expectation delta: **+0.3238 → +0.0476**
- Rubric delta: **+3.0714 → +0.2952**
- Time delta per eval: **−4.8095 s → +5.3333 s**
- Executable delta: **+0.3667 → +0.0917**

Interpretation: this large regression is overwhelmingly explained by blind-comparator access failures in this iteration, not by a plausible overnight collapse of the skill itself.

---

## 7. Verdict

**Verdict: inconclusive for skill quality; conclusive for benchmark-execution instability.**

The run shows one clear with-skill win and otherwise blocked comparisons. Treat this as a workflow reliability signal: fix blind comparator access first, then rerun before making product-level decisions about the `likec4-dsl` skill quality trend.
