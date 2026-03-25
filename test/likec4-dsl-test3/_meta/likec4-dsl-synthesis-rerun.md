# Critical Synthesis — `likec4-dsl` Benchmark

**Iteration:** `likec4-dsl-test3`  
**Protocol:** `benchmark-v2`  
**Evals:** 21 (ids 0–20), 1 run per configuration  
**Generated:** 2026-03-25

---

## 1. Quantitative results

| Metric | `with_skill` | `without_skill` | Δ |
| --- | --- | --- | --- |
| **Blind win rate** | **18/21 = 85.71%** | 2/21 = 9.52% | **+76.19 pp** |
| **Expectation pass rate** | **0.9619** | 0.6667 | **+0.2952** |
| **Rubric score (0–10)** | **9.2857** | 6.4048 | **+2.8809** |
| Seconds / eval | 16.2381 s | **10.9048 s** | +5.3333 s |
| Words / eval | 68.2857 | **66.9524** | +1.3333 |
| Files read | 21.0 | **0.0** | +21.0 |
| **Executable validity** | **0.6250** | 0.5333 | **+0.0917** |

Overall signal: **strong quality win for `with_skill`, with a real but acceptable efficiency cost**. The rerun replaced the earlier blind-access failure pattern with fully discriminating evidence, and the skill now shows clear gains on blind judgments, expectation coverage, rubric quality, and executable validity.

---

## 2. Eval-by-eval analysis

| Eval | Topic | Winner | Key discriminator |
| --- | --- | --- | --- |
| 0 | targeted validate command | with_skill | Correct CLI shape plus `filteredFiles` / `filteredErrors` interpretation |
| 1 | config include paths | with_skill | Better explanation of nearest-config project ownership |
| 2 | export png flags | with_skill | Closer match to expected `npx likec4 export png` flag set |
| 3 | dynamic sequence syntax | with_skill | Included `variant sequence` and explicit return arrows `<-` |
| 4 | view-level styling scope | without_skill | Better rule ordering for mute-then-highlight view styling |
| 5 | deployment instances | with_skill | Used correct `instanceOf` deployment syntax |
| 6 | scoped predicate semantics | with_skill | Correct distinction between `_`, `*`, and `**` semantics |
| 7 | extends + scope inheritance | with_skill | More accurate inherited-scope view extension pattern |
| 8 | global predicateGroup reuse | with_skill | Used the expected reusable global `predicateGroup` mechanism |
| 9 | chained + parallel dynamic | with_skill | Correct explicit parallel fan-out block in the dynamic view |
| 10 | deployment tag inheritance | tie | Both answers correctly explained inherited plus instance-local tags |
| 11 | extend metadata merge | with_skill | Correct metadata merge semantics for duplicate keys |
| 12 | deployment view limits | with_skill | Cleaner and more focused explanation of unsupported deployment-view styling |
| 13 | tag/property ordering | with_skill | Correctly fixed tag-before-property ordering |
| 14 | invalid top-level styles | with_skill | More complete explanation of valid top-level blocks |
| 15 | identifier validity rules | with_skill | Correct validity judgments for dotted, dashed, and numeric-leading ids |
| 16 | parent-child relationship invalidity | without_skill | Slightly stronger explanation of containment vs explicit relationships |
| 17 | cross-file FQN resolution | with_skill | Clearer lexical-scope explanation and better fully-qualified rewrite |
| 18 | relationship extend matching | with_skill | Better explanation of relationship identity matching requirements |
| 19 | scoped `*` semantics | with_skill | More precise direct-children interpretation for scoped wildcard include |
| 20 | two-file validate command | with_skill | Exact two-file CLI pattern and correct scoped JSON verification |

### Observations

- `with_skill` wins **18** evals and loses only **2**, with **1** tie.
- The strongest recurring advantage is **syntax precision**: the skill consistently nudges answers toward the exact LikeC4 DSL or CLI form expected by the eval.
- The second major advantage is **semantic specificity**: several wins come from explaining nuanced behavior correctly rather than just producing plausible-looking syntax.
- The two losses are narrow and localized rather than systemic.

---

## 3. Executable validity analysis

Executable validity improved from **0.5333** to **0.6250** (+0.0917) for `with_skill`.

This is a useful confirmation signal: the skill does not only improve blind judgments, it also produces slightly more structurally valid LikeC4 snippets. That said, the gain is smaller than the blind win-rate gain, which suggests the skill’s biggest benefit is not merely “syntactic validity”, but **better task targeting and more correct explanations of DSL semantics**.

There is still room to improve executable robustness. A 62.5% valid-eval rate is positive but not yet best-in-class for a focused DSL skill.

---

## 4. Skill design assessment

### Strengths

- Strong on **exact command construction** for validation/export tasks.
- Strong on **subtle DSL semantics** (`predicate` scope, metadata merge behavior, identifier validity, relationship matching).
- Good at **minimal corrective snippets** that stay close to the asked fix.
- Produces clear blind wins on both **expectation coverage** and **rubric quality**.

### Weaknesses

- Efficiency cost is now visible: `with_skill` is **slower** (+5.3333 s/eval) and slightly more verbose.
- Executable-validity gains are real but modest relative to the large blind-quality gains.
- A few presentation/style-oriented tasks still allow baseline to edge ahead when ordering or visual-effect framing matters.

---

## 5. Priority recommendations

**P1 — Critical**
- Improve instructions around **view styling order/effect precedence**, especially for one-off highlighting patterns like the loss on eval 4.
- Improve guidance for **relationship-vs-containment explanation quality**, since eval 16 shows the baseline can still edge ahead on conceptual framing.

**P2 — Important**
- Add sharper executable examples for deployment/view-related tasks to push executable validity beyond the current 62.5%.
- Trim answer scaffolding where possible to recover some of the current speed penalty without losing DSL precision.

**P3 — Nice to have**
- Add a second run to measure variance now that blind evidence is stable again.
- Extend examples for style-focused tasks and edge-case semantics so the few close losses become cleaner wins.

---

## 6. Previous-run comparison (`likec4-dsl-test2` → `likec4-dsl-test3`)

Key deltas vs previous run:

- Blind win rate: **95.24% → 85.71%** (−9.53 pp)
- Expectation delta: **+0.3238 → +0.2952**
- Rubric delta: **+3.0714 → +2.8809**
- Time delta per eval: **−4.8095 s → +5.3333 s**
- Executable delta: **+0.3667 → +0.0917**

Interpretation: the skill is still clearly beneficial, but this rerun shows a **less dominant and more expensive** win profile than `likec4-dsl-test2`. The biggest regression is efficiency: the previous run was faster with skill, whereas this rerun is slower. Quality remains decisively positive, but the margin has narrowed.

---

## 7. Verdict

**Verdict: strong positive skill impact, with moderate efficiency regression.**

After rerunning blind compare with accessible evidence, `likec4-dsl` shows a trustworthy and substantial advantage: **18 wins out of 21**, materially better expectation coverage, materially better rubric scores, and slightly better executable validity. The remaining issues are refinement problems, not evidence-access noise.

In short: the blind rerun rescues the iteration from the earlier bogus state, and the resulting benchmark now supports a clear conclusion — **the skill helps, but it currently buys quality with extra time and only modest executable-validity improvement.**
