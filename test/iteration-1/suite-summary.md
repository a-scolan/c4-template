# Skill Suite Summary — iteration-1

Generated at: 2026-03-17T09:27:55Z
Previous iteration: None found
Protocol version: benchmark-v2
Skill count: 19

## Metric validation

Status: passed
Files checked: 38/38
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
| With-skill win rate | 0.870 | 0.178 | 0.333 | 1.000 |
| Expectation Δ | 0.248 | 0.154 | 0.028 | 0.667 |
| Rubric Δ | 1.718 | 1.082 | -0.100 | 4.500 |
| Time Δ / eval | 1.824 | 49.350 | -33.600 | 198.667 |
| Executable Δ | -0.667 | 0.577 | -1.000 | 0.000 |


## Suite overview

All required run-metrics files were present and complete.

| Skill | Evals | Runs | With-skill win rate | Expectation Δ | Rubric Δ | Time Δ / eval (s) | Executable Δ | Words Δ / eval | Files read Δ | High-var evals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 6 | 1 | 83.3% | 0.097 | 0.400 | -7.333 | - | -1.0 | 2.0 | 0 |
| configure-project-includes | 6 | 1 | 83.3% | 0.200 | 1.317 | -10.667 | - | -5.5 | 2.0 | 0 |
| create-element | 5 | 1 | 80.0% | 0.230 | 2.400 | -33.600 | - | 39.0 | 5.0 | 0 |
| create-relationship | 5 | 1 | 60.0% | 0.200 | 1.400 | -12.800 | - | -3.6 | 2.0 | 0 |
| create-sequence-view | 4 | 1 | 100.0% | 0.312 | 1.925 | -3.500 | -1.000 | -12.0 | 2.0 | 0 |
| customize-view | 5 | 1 | 100.0% | 0.247 | 1.640 | -31.800 | 0.000 | 8.4 | 2.0 | 0 |
| design-view | 4 | 1 | 75.0% | 0.417 | 2.750 | -11.750 | - | -7.8 | 3.0 | 0 |
| document-decision | 3 | 1 | 100.0% | 0.150 | 2.100 | 0.333 | - | 177.7 | 2.0 | 0 |
| implement-pattern | 4 | 1 | 100.0% | 0.312 | 2.100 | -0.250 | -1.000 | 57.8 | 2.0 | 0 |
| lookup-element-kinds | 5 | 1 | 100.0% | 0.400 | 2.740 | -16.600 | - | 0.2 | 7.0 | 0 |
| model-deployment-infrastructure | 5 | 1 | 100.0% | 0.230 | 1.560 | -0.800 | - | 51.2 | 3.0 | 0 |
| name-deployment-nodes | 3 | 1 | 100.0% | 0.445 | 2.900 | 25.667 | - | -2.0 | 2.0 | 0 |
| organize-multi-project | 4 | 1 | 100.0% | 0.250 | 1.550 | -9.000 | - | 30.0 | 2.0 | 0 |
| structure-deployment-tiers | 3 | 1 | 100.0% | 0.111 | 1.333 | 198.667 | - | 79.0 | 2.0 | 0 |
| sync-with-template | 5 | 1 | 80.0% | 0.240 | 1.240 | -16.000 | - | 25.8 | 2.0 | 0 |
| test-model | 3 | 1 | 33.3% | 0.028 | -0.100 | 3.333 | - | -15.0 | 2.0 | 0 |
| troubleshoot-errors | 4 | 1 | 75.0% | 0.083 | 0.350 | -14.250 | - | 43.2 | -2.0 | 0 |
| understand-project-structure | 6 | 1 | 83.3% | 0.100 | 0.533 | -10.000 | - | -41.3 | 8.0 | 0 |
| write-rich-descriptions | 3 | 1 | 100.0% | 0.667 | 4.500 | -15.000 | - | 10.3 | 2.0 | 0 |

## Per-skill detailed comparison

| Skill | Runs | Exp pass with | Exp pass without | Rubric with | Rubric without | Sec/eval with | Sec/eval without | Exec with | Exec without | Words/eval with | Words/eval without | Files read with | Files read without |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 1 | 0.917 | 0.820 | 9.167 | 8.767 | 10.333 | 17.667 | - | - | 84.5 | 85.5 | 2.0 | 0.0 |
| configure-project-includes | 1 | 0.967 | 0.767 | 9.133 | 7.817 | 24.333 | 35.000 | 0.000 | - | 76.3 | 81.8 | 2.0 | 0.0 |
| create-element | 1 | 0.920 | 0.690 | 9.400 | 7.000 | 56.800 | 90.400 | 0.000 | - | 88.6 | 49.6 | 5.0 | 0.0 |
| create-relationship | 1 | 0.920 | 0.720 | 9.160 | 7.760 | 22.000 | 34.800 | 0.000 | - | 74.2 | 77.8 | 2.0 | 0.0 |
| create-sequence-view | 1 | 1.000 | 0.688 | 9.725 | 7.800 | 35.250 | 38.750 | 0.000 | 1.000 | 94.5 | 106.5 | 2.0 | 0.0 |
| customize-view | 1 | 0.920 | 0.673 | 9.000 | 7.360 | 23.800 | 55.600 | 0.000 | 0.000 | 38.2 | 29.8 | 2.0 | 0.0 |
| design-view | 1 | 0.625 | 0.208 | 7.500 | 4.750 | 39.500 | 51.250 | 0.750 | - | 114.8 | 122.5 | 3.0 | 0.0 |
| document-decision | 1 | 0.739 | 0.589 | 8.733 | 6.633 | 38.333 | 38.000 | - | - | 296.0 | 118.3 | 2.0 | 0.0 |
| implement-pattern | 1 | 0.854 | 0.542 | 8.700 | 6.600 | 39.500 | 39.750 | 0.000 | 1.000 | 135.5 | 77.8 | 2.0 | 0.0 |
| lookup-element-kinds | 1 | 1.000 | 0.600 | 9.140 | 6.400 | 37.400 | 54.000 | - | - | 105.2 | 105.0 | 7.0 | 0.0 |
| model-deployment-infrastructure | 1 | 0.960 | 0.730 | 9.180 | 7.620 | 32.400 | 33.200 | - | - | 134.8 | 83.6 | 3.0 | 0.0 |
| name-deployment-nodes | 1 | 1.000 | 0.555 | 9.333 | 6.433 | 62.000 | 36.333 | - | - | 77.7 | 79.7 | 2.0 | 0.0 |
| organize-multi-project | 1 | 0.812 | 0.562 | 8.850 | 7.300 | 24.500 | 33.500 | - | - | 114.8 | 84.8 | 2.0 | 0.0 |
| structure-deployment-tiers | 1 | 0.917 | 0.806 | 9.400 | 8.067 | 237.000 | 38.333 | 1.000 | - | 171.3 | 92.3 | 2.0 | 0.0 |
| sync-with-template | 1 | 0.910 | 0.670 | 8.760 | 7.520 | 30.000 | 46.000 | - | - | 127.8 | 102.0 | 2.0 | 0.0 |
| test-model | 1 | 0.806 | 0.778 | 8.400 | 8.500 | 46.333 | 43.000 | - | - | 177.0 | 192.0 | 2.0 | 0.0 |
| troubleshoot-errors | 1 | 0.917 | 0.833 | 9.100 | 8.750 | 37.250 | 51.500 | - | - | 146.8 | 103.5 | 3.0 | 5.0 |
| understand-project-structure | 1 | 0.792 | 0.692 | 8.617 | 8.083 | 26.833 | 36.833 | - | - | 87.8 | 129.2 | 8.0 | 0.0 |
| write-rich-descriptions | 1 | 0.833 | 0.167 | 8.800 | 4.300 | 24.333 | 39.333 | - | - | 90.7 | 80.3 | 2.0 | 0.0 |

## High-variance evals

No high-variance evals were flagged.

## Previous-iteration comparison

No previous iteration was found for comparison.
