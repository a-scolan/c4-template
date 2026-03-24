# Skill Suite Summary — likec4-dsl-test

Generated at: 2026-03-24T15:18:09Z
Previous iteration: None found
Protocol version: benchmark-v2
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
| With-skill win rate | 1.000 | 0.000 | 1.000 | 1.000 |
| Expectation Δ | 0.300 | 0.000 | 0.300 | 0.300 |
| Rubric Δ | 3.833 | 0.000 | 3.833 | 3.833 |
| Time Δ / eval | -8.167 | 0.000 | -8.167 | -8.167 |
| Executable Δ | -0.100 | 0.000 | -0.100 | -0.100 |


## Suite overview

All required run-metrics files were present and complete.

| Skill | Evals | Runs | With-skill win rate | Expectation Δ | Rubric Δ | Time Δ / eval (s) | Executable Δ | Words Δ / eval | Files read Δ | High-var evals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 6 | 1 | 100.0% | 0.300 | 3.833 | -8.167 | -0.100 | -26.2 | 0.0 | 0 |

## Per-skill detailed comparison

| Skill | Runs | Exp pass with | Exp pass without | Rubric with | Rubric without | Sec/eval with | Sec/eval without | Exec with | Exec without | Words/eval with | Words/eval without | Files read with | Files read without |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 1 | 1.000 | 0.700 | 9.667 | 5.833 | 41.167 | 49.333 | 0.500 | 0.600 | 85.7 | 111.8 | 6.0 | 6.0 |

## High-variance evals

No high-variance evals were flagged.

## Previous-iteration comparison

No previous iteration was found for comparison.
