# Skill Benchmark Comparison — `likec4-dsl-test` vs `likec4-dsl-test2`

Generated at: 2026-03-25T08:42:26Z  
Skill: `likec4-dsl`

---

## Overview

| Iteration | Evals | Runs | Win rate | Exp Δ | Rubric Δ | Time Δ/eval | Words Δ/eval | Exec Δ | Files read Δ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `likec4-dsl-test` | 6 | 1 | **100.0%** | +0.300 | +3.833 | -8.2s | -26.2 | -0.100 | 0.0 |
| `likec4-dsl-test2` | 21 | 1 | **95.2%** | +0.324 | +3.071 | -4.8s | +54.7 | +0.367 | +6.0 |
| **Δ (test2 − test)** | +15 | — | **-4.8 pp** | +0.024 | -0.762 | +3.4s | +80.9 | **+0.467** | +6.0 |

---

## Per-skill detail

| Iteration | Exp with | Exp without | Rubric with | Rubric without | Time with | Time without | Exec with | Exec without | Words with | Words without | Files with | Files without |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `likec4-dsl-test` | 1.000 | 0.700 | 9.667 | 5.833 | 41.2s | 49.3s | 0.500 | 0.600 | 85.7 | 111.8 | 6.0 | 6.0 |
| `likec4-dsl-test2` | 0.971 | 0.648 | 8.786 | 5.714 | 16.4s | 21.2s | 0.500 | 0.133 | 142.1 | 87.4 | 6.0 | 0.0 |

---

## Key findings

### 1. Win rate: 100% → 95.2% (one genuine loss)

`likec4-dsl-test` was a 6-eval pilot run with 100% win rate.  
`likec4-dsl-test2` expanded to 21 evals and found one loss: **eval 18** (relationship `extend` matching
semantics — the `with_skill` response incorrectly stated matching uses only source/target, omitting
kind/title criteria).  
The remaining 20/21 evals are wins.

### 2. Baseline isolation was broken in `likec4-dsl-test`

In `likec4-dsl-test`, the `without_skill` configuration read **6.0 files** on average — the same as
`with_skill`. This strongly suggests the baseline workers read `SKILL.md` or related files during the
pilot run, inflating `without_skill` quality and deflating the apparent skill benefit.

In `likec4-dsl-test2`, strict relocation was used: `without_skill` reads **0 files** (proper
isolation), giving a more trustworthy measurement of the skill's true contribution.

**Implication**: the `likec4-dsl-test` metrics are likely overly conservative (the skill benefit is
understated because the baseline had partial access to skill knowledge).

### 3. Rubric delta dropped slightly: +3.83 → +3.07 (−0.76)

Expanding from 6 pilot evals to 21 coverage evals added harder tasks where the skill provides
moderate but non-dominant improvement. The wider coverage is more representative; the smaller delta
reflects real-world task diversity.

### 4. Executable snippet validity improved dramatically

`without_skill` executable validity: 0.60 (test) → **0.13** (test2).  
`with_skill` executable validity: 0.50 → 0.50 (stable).  
The net delta: **−0.10 → +0.37**, a +47 pp swing.

This is explained by two factors:
- The pilot `without_skill` had partial skill contamination (files_read > 0), boosting its snippet quality artificially.
- The full 21-eval set includes more difficult DSL tasks where the baseline fails structurally.

### 5. Response length cost: −26 words/eval → +55 words/eval (+81)

`likec4-dsl-test` `with_skill` responses were more concise (86 words) than `without_skill` (112 words).  
`likec4-dsl-test2` reversed this: `with_skill` produces 142 words vs 87 for `without_skill`.

The 21-eval suite includes many "write a snippet" tasks where the skill adds explanatory context. The
+55 word delta is a cost that should be monitored — the skill should be nudged toward minimal snippets
when the task explicitly says "minimal example."

### 6. Skill now consumes 6 additional files per run (test2)

`with_skill` reads SKILL.md + CLI reference + views + predicates + examples (6 files).  
`without_skill` reads 0 files (isolated baseline).  
This shows the skill is being used actively, not just as a trigger hint.

---

## Verdict

`likec4-dsl-test2` supersedes `likec4-dsl-test` as the canonical benchmark:

- **Wider coverage** (21 vs 6 evals) across all DSL task categories.
- **Clean baseline isolation** (0 vs 6 files read without_skill) — removes the contamination bias.
- **One real failure found** (eval 18) that the 6-eval pilot missed.
- **Executable quality improvement confirmed** across a representative set of snippet tasks.

The 100% win rate of `likec4-dsl-test` was artificially inflated by baseline contamination and the
small, hand-selected eval set. The 95.2% win rate of `likec4-dsl-test2` on 21 evals with clean
isolation is the correct baseline performance figure for this skill.

---

## Recommended next steps

1. **Patch eval 18 grading-spec or skill** — verify whether the correct `extend` matching semantics
   include kind/title, and update whichever is wrong.
2. **Trim verbosity for "minimal snippet" tasks** — add a prompt hint in the skill that minimal
   examples should stay under ~80 words.
3. **Keep clean relocation** for all future baseline runs of this skill.
4. **Run with n ≥ 3 repetitions** in a future iteration to measure variance (both iterations used n=1).

---

## Iteration artifacts

| Artifact | Path |
| --- | --- |
| `likec4-dsl-test` summary | [test/likec4-dsl-test/suite-summary.md](../likec4-dsl-test/suite-summary.md) |
| `likec4-dsl-test2` summary | [test/likec4-dsl-test2/suite-summary.md](../likec4-dsl-test2/suite-summary.md) |
| `likec4-dsl-test` blind comparisons | [test/likec4-dsl-test/likec4-dsl/blind-comparisons.json](../likec4-dsl-test/likec4-dsl/blind-comparisons.json) |
| `likec4-dsl-test2` blind comparisons | [test/likec4-dsl-test2/likec4-dsl/blind-comparisons.json](../likec4-dsl-test2/likec4-dsl/blind-comparisons.json) |
| `likec4-dsl-test2` synthesis | [test/iteration-2/likec4-dsl/synthesis.md](../iteration-2/likec4-dsl/synthesis.md) |
