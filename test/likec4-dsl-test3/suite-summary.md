# Skill Suite Summary — likec4-dsl-test3

Generated at: 2026-03-25T20:03:28Z
Previous iteration: likec4-dsl-test2
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
| With-skill win rate | 0.857 | 0.000 | 0.857 | 0.857 |
| Expectation Δ | 0.295 | 0.000 | 0.295 | 0.295 |
| Rubric Δ | 2.881 | 0.000 | 2.881 | 2.881 |
| Time Δ / eval | 5.333 | 0.000 | 5.333 | 5.333 |
| Executable Δ | 0.092 | 0.000 | 0.092 | 0.092 |


## Suite overview

All required run-metrics files were present and complete.

| Skill | Evals | Runs | With-skill win rate | Expectation Δ | Rubric Δ | Time Δ / eval (s) | Executable Δ | Words Δ / eval | Files read Δ | High-var evals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 21 | 1 | 85.7% | 0.295 | 2.881 | 5.333 | 0.092 | 1.3 | 21.0 | 0 |

## Per-skill detailed comparison

| Skill | Runs | Exp pass with | Exp pass without | Rubric with | Rubric without | Sec/eval with | Sec/eval without | Exec with | Exec without | Words/eval with | Words/eval without | Files read with | Files read without |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 1 | 0.962 | 0.667 | 9.286 | 6.405 | 16.238 | 10.905 | 0.625 | 0.533 | 68.3 | 67.0 | 21.0 | 0.0 |

## High-variance evals

No high-variance evals were flagged.

## Previous-iteration comparison

| Skill | Prev win rate | Curr win rate | Δ win rate | Prev expectation Δ | Curr expectation Δ | Δ expectation Δ | Prev time Δ / eval | Curr time Δ / eval | Δ time Δ / eval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| likec4-dsl | 95.2% | 85.7% | -0.095 | 0.324 | 0.295 | -0.029 | -4.809 | 5.333 | 10.143 |
