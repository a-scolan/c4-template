# Skill Suite Summary — likec4-dsl-test5

Generated at: 2026-03-30T14:46:14Z
Previous iteration: likec4-dsl-test4
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
| With-skill win rate | 0.759 | 0.000 | 0.759 | 0.759 |
| Expectation Δ | 0.209 | 0.000 | 0.209 | 0.209 |
| Rubric Δ | 1.845 | 0.000 | 1.845 | 1.845 |
| Time Δ / eval | -0.103 | 0.000 | -0.103 | -0.103 |
| Executable Δ | 0.085 | 0.000 | 0.085 | 0.085 |


## Suite overview

All required run-metrics files were present and complete.

| Skill | Evals | Runs | With-skill win rate | Expectation Δ | Rubric Δ | Time Δ / eval (s) | Executable Δ | Words Δ / eval | Files read Δ | High-var evals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 29 | 2 | 75.9% | 0.209 | 1.845 | -0.103 | 0.085 | -182.4 | 0.0 | 29 |

## Per-skill detailed comparison

| Skill | Runs | Exp pass with | Exp pass without | Rubric with | Rubric without | Sec/eval with | Sec/eval without | Exec with | Exec without | Words/eval with | Words/eval without | Files read with | Files read without |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 2 | 0.972 | 0.764 | 9.259 | 7.414 | 0.000 | 0.103 | 0.667 | 0.582 | 53.8 | 236.2 | 29.0 | 29.0 |

## High-variance evals

| Skill | Source | Eval | Run count | Winner flips | Expectation stddev | Rubric stddev |
| --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | with_skill | 21 | - | no | - | - |
| likec4-dsl | with_skill | 24 | - | no | - | - |
| likec4-dsl | without_skill | 0 | - | no | - | - |
| likec4-dsl | without_skill | 1 | - | no | - | - |
| likec4-dsl | without_skill | 2 | - | no | - | - |
| likec4-dsl | without_skill | 4 | - | no | - | - |
| likec4-dsl | without_skill | 5 | - | no | - | - |
| likec4-dsl | without_skill | 10 | - | no | - | - |
| likec4-dsl | without_skill | 11 | - | no | - | - |
| likec4-dsl | without_skill | 12 | - | no | - | - |
| likec4-dsl | without_skill | 13 | - | no | - | - |
| likec4-dsl | without_skill | 15 | - | no | - | - |
| likec4-dsl | without_skill | 17 | - | no | - | - |
| likec4-dsl | without_skill | 18 | - | no | - | - |
| likec4-dsl | blind | 0 | 2 | no | 0.000 | 1.414 |
| likec4-dsl | blind | 6 | 2 | yes | 0.707 | 4.596 |
| likec4-dsl | blind | 9 | 2 | yes | 0.000 | 0.707 |
| likec4-dsl | blind | 10 | 2 | no | 0.424 | 2.616 |
| likec4-dsl | blind | 12 | 2 | yes | 0.000 | 0.283 |
| likec4-dsl | blind | 13 | 2 | no | 0.283 | 2.051 |
| likec4-dsl | blind | 15 | 2 | no | 0.141 | 1.980 |
| likec4-dsl | blind | 17 | 2 | yes | 0.000 | 0.283 |
| likec4-dsl | blind | 18 | 2 | yes | 0.000 | 1.061 |
| likec4-dsl | blind | 19 | 2 | no | 0.236 | 0.000 |
| likec4-dsl | blind | 21 | 2 | yes | 0.000 | 0.919 |
| likec4-dsl | blind | 22 | 2 | yes | 0.000 | 0.424 |
| likec4-dsl | blind | 25 | 2 | yes | 0.424 | 3.323 |
| likec4-dsl | blind | 26 | 2 | yes | 0.141 | 1.485 |
| likec4-dsl | blind | 27 | 2 | no | 0.000 | 1.202 |

## Previous-iteration comparison

| Skill | Prev win rate | Curr win rate | Δ win rate | Prev expectation Δ | Curr expectation Δ | Δ expectation Δ | Prev time Δ / eval | Curr time Δ / eval | Δ time Δ / eval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 79.3% | 75.9% | -0.035 | 0.271 | 0.209 | -0.062 | 14.414 | -0.103 | -14.517 |
