# Skill Suite Summary — likec4-dsl-test9

Generated at: 2026-03-31T14:05:38Z
Previous iteration: likec4-dsl-test8
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
| With-skill win rate | 0.812 | 0.000 | 0.812 | 0.812 |
| Expectation Δ | 0.279 | 0.000 | 0.279 | 0.279 |
| Rubric Δ | 2.684 | 0.000 | 2.684 | 2.684 |
| Time Δ / eval | -4.756 | 0.000 | -4.756 | -4.756 |
| Executable Δ | 0.003 | 0.000 | 0.003 | 0.003 |


## Suite overview

All required run-metrics files were present and complete.

| Skill | Evals | Runs | With-skill win rate | Expectation Δ | Rubric Δ | Time Δ / eval (s) | Executable Δ | Words Δ / eval | Files read Δ | High-var evals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 32 | 2 | 81.2% | 0.279 | 2.684 | -4.756 | 0.003 | -13.0 | 0.0 | 21 |

## Per-skill detailed comparison

| Skill | Runs | Exp pass with | Exp pass without | Rubric with | Rubric without | Sec/eval with | Sec/eval without | Exec with | Exec without | Words/eval with | Words/eval without | Files read with | Files read without |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 2 | 0.982 | 0.704 | 9.512 | 6.828 | 27.697 | 32.453 | 0.881 | 0.878 | 77.0 | 90.0 | 32.0 | 32.0 |

## High-variance evals

| Skill | Source | Eval | Run count | Winner flips | Expectation stddev | Rubric stddev |
| --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | with_skill | 14 | - | no | - | - |
| likec4-dsl | with_skill | 15 | - | no | - | - |
| likec4-dsl | with_skill | 24 | - | no | - | - |
| likec4-dsl | without_skill | 7 | - | no | - | - |
| likec4-dsl | without_skill | 8 | - | no | - | - |
| likec4-dsl | without_skill | 10 | - | no | - | - |
| likec4-dsl | without_skill | 14 | - | no | - | - |
| likec4-dsl | without_skill | 15 | - | no | - | - |
| likec4-dsl | without_skill | 18 | - | no | - | - |
| likec4-dsl | without_skill | 31 | - | no | - | - |
| likec4-dsl | blind | 2 | 2 | no | 0.141 | 2.121 |
| likec4-dsl | blind | 4 | 2 | yes | 0.141 | 0.707 |
| likec4-dsl | blind | 6 | 2 | no | 0.000 | 1.061 |
| likec4-dsl | blind | 8 | 2 | no | 0.141 | 1.414 |
| likec4-dsl | blind | 9 | 2 | no | 0.283 | 0.000 |
| likec4-dsl | blind | 12 | 2 | yes | 0.117 | 2.121 |
| likec4-dsl | blind | 14 | 2 | no | 0.141 | 1.414 |
| likec4-dsl | blind | 15 | 2 | no | 0.283 | 2.828 |
| likec4-dsl | blind | 20 | 2 | no | 0.000 | 2.828 |
| likec4-dsl | blind | 21 | 2 | no | 0.566 | 6.152 |
| likec4-dsl | blind | 28 | 2 | yes | 0.000 | 0.707 |

## Previous-iteration comparison

| Skill | Prev win rate | Curr win rate | Δ win rate | Prev expectation Δ | Curr expectation Δ | Δ expectation Δ | Prev time Δ / eval | Curr time Δ / eval | Δ time Δ / eval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 76.6% | 81.2% | 0.047 | 0.214 | 0.279 | 0.065 | -6.600 | -4.756 | 1.845 |
