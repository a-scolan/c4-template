# Skill Suite Summary — likec4-dsl-test8

Generated at: 2026-03-31T11:32:04Z
Previous iteration: likec4-dsl-test7
Protocol version: benchmark-v3
Skill count: 1

## Metric validation

Status: passed
Files checked: 2/2
Issues: 0

## Metric legend

| Metric | Meaning | How to read it |
| --- | --- | --- |
| With-skill win rate | Share of blind comparisons won by the `with_skill` response. | Higher is better for the skill. Ties are not wins. |
| Expectation pass rate | Average share of listed expectations satisfied by a response. | Higher is better. `Expectation Δ = with_skill - without_skill`. |
| Rubric score | Blind comparator overall quality score on a 0-10 scale. | Higher is better. `Rubric Δ = with_skill - without_skill`. |
| Time per eval | Average wall-clock seconds spent per eval. | Lower is faster. `Time Δ = with_skill - without_skill`, so a negative delta means the skill was faster. |
| Words per eval | Average response length in words. | Lower means more concise, but not automatically better unless quality stays strong. |
| Files read count | Count of repository files intentionally read during a run. | Proxy for context consumption. Higher means more repository context was consumed. |
| Executable validity | Share of snippet-bearing eval runs whose LikeC4 snippets passed automated structural checks. | Higher is better. `Executable Δ = with_skill - without_skill`. |

### Reading deltas

- `Expectation Δ > 0`: the skill satisfied more listed expectations.
- `Rubric Δ > 0`: the skill was judged better overall.
- `Time Δ < 0`: the skill was faster.
- `Words Δ < 0`: the skill was more concise.
- `Files read Δ > 0`: the skill consumed more repository context.
- `Executable Δ > 0`: the skill produced more structurally valid LikeC4 snippets.

## Suite variance

| Metric | Mean | Stddev | Min | Max |
| --- | --- | --- | --- | --- |
| With-skill win rate | 0.766 | 0.000 | 0.766 | 0.766 |
| Expectation Δ | 0.214 | 0.000 | 0.214 | 0.214 |
| Rubric Δ | 2.134 | 0.000 | 2.134 | 2.134 |
| Time Δ / eval | -6.600 | 0.000 | -6.600 | -6.600 |
| Executable Δ | 0.066 | 0.000 | 0.066 | 0.066 |


## Suite overview

All required run-metrics files were present and complete.

| Skill | Evals | Runs | With-skill win rate | Expectation Δ | Rubric Δ | Time Δ / eval (s) | Executable Δ | Words Δ / eval | Files read Δ | High-var evals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 32 | 2 | 76.6% | 0.214 | 2.134 | -6.600 | 0.066 | -14.2 | 0.0 | 19 |

## Per-skill detailed comparison

| Skill | Runs | Exp pass with | Exp pass without | Rubric with | Rubric without | Sec/eval with | Sec/eval without | Exec with | Exec without | Words/eval with | Words/eval without | Files read with | Files read without |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 2 | 0.951 | 0.737 | 9.305 | 7.170 | 13.403 | 20.004 | 0.653 | 0.587 | 66.4 | 80.6 | 32.0 | 32.0 |

## High-variance evals

| Skill | Source | Eval | Run count | Winner flips | Expectation stddev | Rubric stddev |
| --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | with_skill | 1 | - | no | - | - |
| likec4-dsl | with_skill | 14 | - | no | - | - |
| likec4-dsl | with_skill | 18 | - | no | - | - |
| likec4-dsl | without_skill | 8 | - | no | - | - |
| likec4-dsl | without_skill | 11 | - | no | - | - |
| likec4-dsl | without_skill | 20 | - | no | - | - |
| likec4-dsl | blind | 1 | 2 | no | 0.141 | 1.414 |
| likec4-dsl | blind | 4 | 2 | yes | 0.000 | 1.061 |
| likec4-dsl | blind | 6 | 2 | no | 0.000 | 1.414 |
| likec4-dsl | blind | 12 | 2 | no | 0.236 | 0.707 |
| likec4-dsl | blind | 14 | 2 | no | 0.141 | 1.273 |
| likec4-dsl | blind | 16 | 2 | yes | 0.000 | 0.212 |
| likec4-dsl | blind | 18 | 2 | yes | 0.141 | 1.414 |
| likec4-dsl | blind | 19 | 2 | no | 0.118 | 1.414 |
| likec4-dsl | blind | 22 | 2 | yes | 0.283 | 3.535 |
| likec4-dsl | blind | 24 | 2 | no | 0.141 | 1.061 |
| likec4-dsl | blind | 27 | 2 | yes | 0.283 | 1.202 |
| likec4-dsl | blind | 28 | 2 | yes | 0.141 | 0.354 |
| likec4-dsl | blind | 29 | 2 | yes | 0.000 | 0.707 |

## Previous-iteration comparison

| Skill | Prev win rate | Curr win rate | Δ win rate | Prev expectation Δ | Curr expectation Δ | Δ expectation Δ | Prev time Δ / eval | Curr time Δ / eval | Δ time Δ / eval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 76.6% | 76.6% | 0.000 | 0.251 | 0.214 | -0.037 | 1.462 | -6.600 | -8.063 |
