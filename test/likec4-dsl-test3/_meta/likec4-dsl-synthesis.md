# Critical Synthesis — `likec4-dsl` Benchmark

**Iteration:** `likec4-dsl-test3`  
**Protocol:** benchmark-v3  
**Evals:** 21 (run-1)  
**Generated:** 2026-03-25

---

## 1. Quantitative results

| Metric | with_skill | without_skill | Δ |
|---|---:|---:|---:|
| Blind win rate | **18/21 = 0.8571** | 2/21 = 0.0952 | **+0.7619** |
| Expectation pass rate | **0.9714** | 0.6667 | **+0.3047** |
| Rubric score (0–10) | **9.3810** | 7.0429 | **+2.3381** |
| Seconds / eval | **8.4286** | 9.4762 | **-1.0476** |
| Words / eval | 72.6190 | **67.7143** | +4.9047 |
| Files read | 6.0 | 0.0 | +6.0 |
| Executable validity | **0.6875** | 0.5714 | **+0.1161** |

Overall signal is strong in favor of `with_skill`: large blind advantage, substantial rubric/expectation lift, and a modest speed edge. The trade-off is slightly higher verbosity and more file reads.

### Comparison with previous run (`likec4-dsl-test2`)

| Metric | test2 | test3 | Δ (test3 - test2) |
|---|---:|---:|---:|
| with_skill win rate | 0.9524 | 0.8571 | -0.0953 |
| expectation delta | 0.3238 | 0.3047 | -0.0191 |
| rubric delta | 3.0714 | 2.3381 | -0.7333 |
| time delta per eval | -4.8095 | -1.0476 | +3.7619 |
| words delta per eval | 54.7142 | 4.9047 | -49.8095 |
| executable delta | 0.3667 | 0.1161 | -0.2506 |

Interpretation: this run is less dominant than test2, but still clearly positive. It appears less over-verbose and less over-optimized for “win at all cost”, with reduced margin but cleaner output length behavior.

---

## 2. Eval-by-eval analysis

| Eval | Topic | Winner | Exp with | Exp without | Key discriminator |
|---|---|---|---:|---:|---|
| 0 | Validate single file + JSON fields | with_skill | 4/5 | 0/5 | Correct filtered-field framing |
| 1 | Multi-config ownership + include paths | with_skill | 4/5 | 3/5 | Better nearest-config explanation |
| 2 | Export CLI exactness | with_skill | 5/5 | 4/5 | Closer expected command form |
| 3 | Dynamic sequence syntax | with_skill | 5/5 | 3/5 | Variant+backward arrows correctness |
| 4 | View-local styling | with_skill | 5/5 | 5/5 | Narrow formatting/precision edge |
| 5 | Deployment instances in VM | with_skill | 5/5 | 4/5 | Cleaner VM instance pattern |
| 6 | `_` vs `*` vs `**` semantics | with_skill | 5/5 | 4/5 | Better predicate semantics |
| 7 | Extends + scope inheritance | with_skill | 5/5 | 4/5 | Incoming predicate precision |
| 8 | Global predicate group reuse | with_skill | 5/5 | 3/5 | Correct reusable global pattern |
| 9 | Chained + parallel dynamic steps | with_skill | 4/5 | 4/5 | Slightly stronger structure fit |
| 10 | Deployment tag inheritance | TIE | 5/5 | 5/5 | Functionally equivalent |
| 11 | `extend` metadata merge behavior | with_skill | 5/5 | 3/5 | Correct merge rationale |
| 12 | Deployment view styling limits | with_skill | 5/5 | 3/5 | Explicit unsupported features |
| 13 | Tag/property ordering fix | with_skill | 5/5 | 2/5 | Correct minimal correction |
| 14 | Invalid top-level `styles` block | with_skill | 5/5 | 2/5 | Valid top-level replacement |
| 15 | Identifier validity edge cases | with_skill | 5/5 | 2/5 | Correct classification and rewrites |
| 16 | Parent-child invalid relationship | without_skill | 5/5 | 5/5 | Baseline judged clearer |
| 17 | Cross-file FQN resolution | with_skill | 5/5 | 5/5 | Better usability, both correct |
| 18 | Kinded relationship `extend` match | without_skill | 5/5 | 5/5 | Baseline judged stricter/clearer |
| 19 | Scoped `*` semantics | with_skill | 5/5 | 4/5 | Better direct-child semantics |
| 20 | Two-file validate filtering | with_skill | 5/5 | 0/5 | Correct exact command + checks |

### Observations

- Biggest discriminators: evals 0, 8, 11, 13, 14, 15, 20.
- Weak/non-discriminating zones: evals 4, 10, 16, 17, 18 (equal expectations or near-equal rubric).
- Two losses (16, 18) indicate precision gaps in relationship-rule pedagogy compared to baseline phrasing.

---

## 3. Executable validity analysis

Executable validity improved (+0.1161), but gain is moderate relative to blind/rubric gains. This suggests the skill improves conceptual correctness more than strict executable snippet quality. The metric is useful but partially noisy: several evals are explanation-heavy and not all contain executable snippets.

---

## 4. Skill design assessment

### Strengths

1. Strong CLI exactness under constrained prompts (`validate`/`export` flags, filtered JSON interpretation).
2. Reliable advanced DSL guidance (`global predicateGroup`, scoped views, dynamic views, deployment caveats).
3. Good correction patterns for invalid DSL snippets and top-level-structure issues.
4. Consistent expectation coverage (0.97 pass rate).

### Weak areas

1. Relationship-rule edge wording can be outperformed by concise baseline phrasing (evals 16, 18).
2. Some wins are narrow and style-driven rather than outcome-driven (evals 4, 9, 17).
3. Deployment semantics still have occasional ambiguity in explanation framing.
4. Executable robustness is improved but not as much as conceptual quality.

---

## 5. Priority recommendations

**P1 — Critical**
- Tighten relationship extension and parent-child prohibition guidance with strict canonical templates (target evals 16, 18).
- Add “must-preserve minimal fix intent” rule for error-correction prompts (avoid solution drift).

**P2 — Important**
- Add compact command-form canonicalization rules for validate/export responses (reduce ambiguous aliases).
- Add explicit “direct children vs descendants” wording macro for scoped wildcard explanations.

**P3 — Nice to have**
- Expand eval set with harder executable checks for dynamic/deployment snippets (parser-validated).
- Add one extra adversarial eval for tie-prone tag inheritance behavior.

---

## 6. Anthropic/Claude quality pass

- **Evidence-first judgment:** Conclusions above are tied to blind winners, rubric deltas, and expectation pass rates from iteration artifacts.
- **No overfitting to one eval:** There are two losses, not one; neither is treated as definitive failure of the skill overall.
- **Discriminating eval quality:** Evals 4/10/16/17/18 are weakly discriminating; improve these with stricter executable or exactness assertions.
- **Useful over verbose:** Win signal is not just verbosity; words delta collapsed from +54.7 (test2) to +4.9 while still preserving strong outcome advantage.
- **Actionable next iteration:** P1/P2/P3 recommendations are concrete, testable, and linked to specific eval evidence.

---

## 7. Verdict

`likec4-dsl` remains clearly effective in `likec4-dsl-test3`: strong blind win rate (0.8571), strong expectation uplift (+0.3047), and robust rubric gain (+2.3381). Compared with `likec4-dsl-test2`, dominance is lower but still substantial, with a healthier verbosity profile. The next iteration should focus on relationship-rule strictness and stronger executable discriminators.