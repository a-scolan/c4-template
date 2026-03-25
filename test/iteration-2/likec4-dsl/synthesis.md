# Critical Synthesis — `likec4-dsl` Benchmark (`iteration-2`)

**Protocol:** `benchmark-v2`  
**Skill:** `likec4-dsl`  
**Iteration folder:** `test/iteration-2/likec4-dsl/`  
**Execution style:** parallel waves with constrained benchmark subagents  
**Language:** English  

---

## Executive summary

This second benchmark run shows that `likec4-dsl` is **strongly beneficial overall**.

Across **21 evals**:

- **Blind win rate:** **95.2%** for `with_skill` ($20/21$ wins)
- **Expectation pass rate:** **0.971** with skill vs **0.648** without skill ($+0.324$)
- **Rubric score:** **8.786 / 10** with skill vs **5.714 / 10** without skill ($+3.071$)
- **Time per eval:** **16.381s** with skill vs **21.191s** without skill ($-4.809$s)
- **Executable validity:** **0.500** with skill vs **0.133** without skill ($+0.367$)

So the skill was not only **more correct**, but also **faster** and **more structurally valid** on snippet-bearing tasks.

The cost is that it produced **longer outputs**:

- **Words per eval:** 142.1 with skill vs 87.4 without skill ($+54.7$)

That is a real trade-off, but the quality gains are large enough that the extra verbosity is justified in this iteration.

---

## What changed versus the previous ad-hoc run

Compared with the earlier `likec4-dsl-test` campaign, this run is materially stronger methodologically:

- it uses a **canonical `iteration-2` folder**, which avoids the old blind-comparator path constraint,
- it was executed with **strict baseline relocation**,
- it used **parallel benchmark subagents** for the scored waves,
- it covered **21 evals instead of 6**, giving a much broader signal,
- and it generated the full post-processing stack (`suite-summary`, `blind-comparisons`, benchmark export, static HTML review).

That makes this iteration much more useful as a real skill-quality checkpoint rather than a spot test.

---

## Phase execution notes

This campaign used the constrained benchmark workers as intended:

- **Baseline phase:** strict relocated baseline after moving all workspace skills out of `.github/skills/`
- **With-skill phase:** fresh targeted workers after restoration
- **Blind phase:** blinded `A/B` comparison workers across all evals

Parallelism was applied as aggressively as the task shape allowed:

- **21 baseline workers** (one per eval prompt)
- **21 with-skill workers** (one per eval prompt)
- **21 blind comparator workers** (one per eval)

That is the maximum practical parallelism for a single-skill iteration while keeping phase boundaries intact.

---

## Quantitative picture

### Core metrics

| Metric | With skill | Without skill | Delta |
|---|---:|---:|---:|
| Blind win rate | **95.2%** | 4.8% | **+90.4 pts** |
| Expectation pass rate | **0.971** | 0.648 | **+0.324** |
| Rubric score | **8.786** | 5.714 | **+3.071** |
| Seconds / eval | **16.381** | 21.191 | **-4.809** |
| Executable validity | **0.500** | 0.133 | **+0.367** |
| Words / eval | 142.1 | **87.4** | **+54.7** |
| Files read | 6.0 | 0.0 | +6.0 |

### Interpretation

The skill is helping in four distinct ways:

1. **Correctness:** expectation pass rate rises by roughly 32 points.
2. **Quality:** rubric score rises by just over 3 points on a 10-point scale.
3. **Speed:** responses arrive faster despite the extra skill context.
4. **DSL reliability:** executable validity improves substantially.

The one downside is **verbosity**. The skill tends to produce fuller explanations, which improves benchmark quality but may be more than some users need in routine cases.

---

## The main pattern: the skill is strongest on exact LikeC4 facts

The skill consistently wins when the task depends on **precise DSL or CLI knowledge that is hard to reconstruct from general intuition**.

That pattern shows up clearly in:

- exact CLI validation/export commands,
- dynamic/sequence view syntax,
- predicate and scoped-view semantics,
- cross-file FQN rules,
- metadata merge behavior,
- deployment-view limitations,
- identifier rules,
- and tag inheritance semantics.

In other words: the skill shines when the answer requires **specific LikeC4 language law**, not just generic architecture taste.

---

## Biggest wins

### 1. CLI correctness remains a major strength

The skill strongly outperformed baseline on the validation/export command tasks.

Examples:

- **Eval 0**: the baseline invented the wrong command family (`check`) and wrong JSON fields; the skill returned the exact `validate --json --no-layout --file ...` form.
- **Eval 2**: the skill used the correct `export png` flags (`--theme dark`, `--flat`, filter, output dir, project path), while baseline drifted into incorrect option names.
- **Eval 20**: the skill correctly used repeated `--file` flags and the right JSON triage fields.

This is exactly the kind of precision users want a DSL skill for.

### 2. Syntax-sensitive DSL tasks improved a lot

The skill clearly helped on tasks that require remembering the exact LikeC4 form rather than approximating it.

Examples:

- **Eval 3**: `variant sequence` plus `<-` response arrows
- **Eval 8**: `predicateGroup` / `global predicate` structure
- **Eval 11**: duplicate metadata keys become arrays
- **Eval 15**: hyphenated identifiers are valid
- **Eval 17**: cross-file nested references must use FQNs

These are all areas where a model without the skill can sound plausible while still being wrong.

### 3. Executable validity improved sharply

`with_skill` reached **0.500** executable-validity rate versus **0.133** baseline.

That is especially encouraging because this metric is stricter than the blind comparator on one dimension: it checks whether snippet-bearing answers survive a structural LikeC4 validity pass. Even though the metric is imperfect, the direction is unambiguously positive here.

---

## The one meaningful loss

The skill appears to lose **one eval out of 21**: **eval 18**.

### Eval 18 — relationship `extend` matching

Prompt summary:
- existing relationship: `frontend -[async]-> api 'streams'`
- proposed extension: `extend frontend -> api 'streams' { metadata { qos 'high' } }`
- task: explain the matching rules and give the correct extension snippet

### Why the skill lost

According to the blind comparison, the losing answer said that relationship extension matching is only by **source and target**, and that kind/title are *not* part of the matcher. The winning answer instead asserted that the correct fix is:

- keep the relationship kind in the matcher,
- and use the more specific form including `-[async]->` and `'streams'`.

This is the single largest risk signal in the iteration, because it suggests one of two things:

1. either the skill’s guidance around relationship `extend` is incomplete or misleading,
2. or the benchmark expectation for this case is too strict / too opinionated relative to actual DSL behavior.

Either way, this eval deserves a targeted follow-up check before fully trusting the current skill text on relationship extension rules.

---

## Areas where the skill is correct but slightly too verbose

The skill often wins by being more explicit, but that explicitness sometimes spills into long-form explanations.

This is visible in:

- evals with already-high correctness on both sides,
- explanation-heavy tasks like tag inheritance, scoped wildcard semantics, and top-level statement validity,
- and tasks where a minimal snippet would have been enough.

This is not a benchmark failure — the skill still wins — but it suggests a future refinement:

> preserve the exactness, but trim non-essential explanation when the user explicitly asks for “minimal” output.

The current skill behaves more like a careful reference guide than a terse expert assistant. That is often good, but not always optimal for UX.

---

## Confidence and limitations

### What is strong in this run

- strict relocated baseline was used,
- benchmark workers were constrained,
- blind comparison covered all 21 evals,
- the post-processing pipeline completed successfully,
- no high-variance evals were flagged.

### What is still limited

- **single run** only (`Runs = 1`), so variance is mechanically low,
- the benchmark does not prove generalization beyond the eval set,
- one critical semantic disagreement exists on relationship `extend` matching,
- previous-iteration comparison for this skill is not available in a meaningful way because the earlier ad-hoc run was not part of the canonical iteration chain.

So this is a **strong iteration**, but not yet the final word.

---

## Recommendations

### High priority

1. **Audit the skill on relationship `extend` matching**
   - Re-read the relevant section in `likec4-dsl` and confirm whether relationship extension matching must include kind/title or not.
   - If the comparator is right, update the skill immediately.
   - If the skill is right and the eval is wrong, revise the grading spec for eval 18.

2. **Keep the CLI reference sections prominent**
   - These evals show some of the biggest gains.
   - CLI exactness is clearly one of the skill’s highest-value contributions.

3. **Preserve the metadata-merge guidance**
   - Eval 11 is a textbook example of why the skill matters.
   - Without the skill, the model confidently gave the wrong merge behavior.

### Medium priority

4. **Trim verbosity in “minimal snippet” tasks**
   - Keep the same correctness level,
   - but bias toward shorter outputs when the prompt explicitly asks for a minimal snippet.

5. **Add one more dedicated eval around relationship extension semantics**
   - The current loss is too important to leave under-specified.
   - A second eval around the same feature would tell us whether this is a real weakness or a single brittle grading case.

### Low priority

6. **Increase repetition count in a future iteration**
   - A run count of $n \ge 3$ would make the resource and quality metrics more publishable.

---

## Final assessment

`likec4-dsl` is performing **very well**.

This iteration strongly supports the claim that the skill adds real value:

- it wins **20 of 21** blind comparisons,
- improves expectation pass rate by **+0.324**,
- improves rubric quality by **+3.071**,
- improves executable validity by **+0.367**,
- and even reduces mean runtime by **~4.8 seconds per eval**.

That is an unusually clean signal.

The one caveat is important but local: **relationship `extend` semantics** should be verified before the skill is treated as fully settled.

So the right conclusion is:

> **Keep the skill, trust it broadly, and patch or re-verify the relationship-extension guidance before the next benchmark iteration.**
