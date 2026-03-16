# Skill Suite Summary — iteration-3

Generated at: 2026-03-13T11:29:01Z
Previous iteration: iteration-2
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
| With-skill win rate | 0.949 | 0.110 | 0.600 | 1.000 |
| Expectation Δ | 0.334 | 0.238 | 0.000 | 0.917 |
| Rubric Δ | 0.865 | 0.986 | 0.008 | 3.467 |
| Time Δ / eval | -2.087 | 5.515 | -23.800 | 1.250 |
| Executable Δ | -0.333 | 0.516 | -1.000 | 0.000 |


## Suite overview

All required run-metrics files were present and complete.

| Skill | Evals | Runs | With-skill win rate | Expectation Δ | Rubric Δ | Time Δ / eval (s) | Executable Δ | Words Δ / eval | Files read Δ | High-var evals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 6 | 1 | 83.3% | 0.083 | 0.225 | -0.833 | - | -25.2 | -13.0 | 0 |
| configure-project-includes | 6 | 1 | 100.0% | 0.200 | 0.587 | 0.000 | - | 1.5 | -9.0 | 0 |
| create-element | 5 | 1 | 100.0% | 0.300 | 1.132 | -4.000 | -1.000 | 34.0 | -4.0 | 0 |
| create-relationship | 5 | 1 | 100.0% | 0.080 | 0.920 | -4.000 | 0.000 | 40.6 | -2.0 | 0 |
| create-sequence-view | 4 | 1 | 100.0% | 0.229 | 0.207 | 0.250 | 0.000 | -12.8 | -6.0 | 0 |
| customize-view | 5 | 1 | 80.0% | 0.430 | 2.660 | -1.400 | 0.000 | 15.4 | -11.0 | 0 |
| design-view | 4 | 1 | 100.0% | 0.562 | 0.328 | -0.750 | 0.000 | -59.8 | -8.0 | 0 |
| document-decision | 3 | 1 | 100.0% | 0.261 | 0.183 | -1.667 | - | 67.3 | 0.0 | 0 |
| implement-pattern | 4 | 1 | 100.0% | 0.312 | 1.575 | 0.500 | -1.000 | 48.5 | -4.0 | 0 |
| lookup-element-kinds | 5 | 1 | 60.0% | 0.000 | 0.008 | -3.800 | - | -9.4 | -6.0 | 0 |
| model-deployment-infrastructure | 5 | 1 | 80.0% | 0.280 | 0.178 | -23.800 | - | 3.8 | -1.0 | 0 |
| name-deployment-nodes | 3 | 1 | 100.0% | 0.917 | 0.653 | 0.667 | - | -19.7 | -4.0 | 0 |
| organize-multi-project | 4 | 1 | 100.0% | 0.250 | 0.100 | 1.250 | - | -18.8 | -3.0 | 0 |
| structure-deployment-tiers | 3 | 1 | 100.0% | 0.193 | 0.123 | 0.000 | - | -12.0 | -2.0 | 0 |
| sync-with-template | 5 | 1 | 100.0% | 0.250 | 1.880 | -2.400 | - | 2.8 | -5.0 | 0 |
| test-model | 3 | 1 | 100.0% | 0.777 | 0.293 | 0.000 | - | 38.0 | -10.0 | 0 |
| troubleshoot-errors | 4 | 1 | 100.0% | 0.165 | 0.090 | 1.000 | - | 34.8 | -6.0 | 0 |
| understand-project-structure | 6 | 1 | 100.0% | 0.475 | 1.817 | 0.667 | - | -26.0 | -2.0 | 0 |
| write-rich-descriptions | 3 | 1 | 100.0% | 0.583 | 3.467 | -1.333 | - | -17.0 | -5.0 | 0 |

## Per-skill detailed comparison

| Skill | Runs | Exp pass with | Exp pass without | Rubric with | Rubric without | Sec/eval with | Sec/eval without | Exec with | Exec without | Words/eval with | Words/eval without | Files read with | Files read without |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 1 | 1 | 0.917 | 4.755 | 4.530 | 0.833 | 1.667 | - | 1.000 | 71.5 | 96.7 | 2 | 15 |
| configure-project-includes | 1 | 1 | 0.800 | 4.812 | 4.225 | 0.167 | 0.167 | - | - | 83.2 | 81.7 | 3 | 12 |
| create-element | 1 | 1 | 0.700 | 4.936 | 3.804 | 2.000 | 6.000 | 0.000 | 1.000 | 73.0 | 39.0 | 5 | 9 |
| create-relationship | 1 | 1.000 | 0.920 | 9.840 | 8.920 | 2.000 | 6.000 | 0.000 | 0.000 | 97.4 | 56.8 | 8 | 10 |
| create-sequence-view | 1 | 1.000 | 0.771 | 0.968 | 0.760 | 1.500 | 1.250 | 0.000 | 0.000 | 97.0 | 109.8 | 2 | 8 |
| customize-view | 1 | 0.960 | 0.530 | 8.800 | 6.140 | 0.600 | 2.000 | 0.000 | 0.000 | 37.0 | 21.6 | 4 | 15 |
| design-view | 1 | 1.000 | 0.438 | 0.965 | 0.637 | 1.250 | 2.000 | 0.000 | 0.000 | 109.5 | 169.2 | 5 | 13 |
| document-decision | 1 | 1.000 | 0.739 | 0.960 | 0.777 | 1.667 | 3.333 | - | - | 225.7 | 158.3 | 2 | 2 |
| implement-pattern | 1 | 1.000 | 0.688 | 9.700 | 8.125 | 2.000 | 1.500 | 0.000 | 1.000 | 149.0 | 100.5 | 7 | 11 |
| lookup-element-kinds | 1 | 1.000 | 1.000 | 0.962 | 0.954 | 0.200 | 4.000 | - | - | 95.6 | 105.0 | 10 | 16 |
| model-deployment-infrastructure | 1 | 1.000 | 0.720 | 0.972 | 0.794 | 0.200 | 24.000 | - | 0.000 | 125.0 | 121.2 | 3 | 4 |
| name-deployment-nodes | 1 | 1.000 | 0.083 | 0.980 | 0.327 | 0.667 | 0.000 | - | - | 73.7 | 93.3 | 2 | 6 |
| organize-multi-project | 1 | 1.000 | 0.750 | 0.968 | 0.868 | 3.000 | 1.750 | - | - | 80.0 | 98.8 | 6 | 9 |
| structure-deployment-tiers | 1 | 1.000 | 0.807 | 0.970 | 0.847 | 2.333 | 2.333 | - | - | 103.3 | 115.3 | 2 | 4 |
| sync-with-template | 1 | 1.000 | 0.750 | 9.660 | 7.780 | 1.000 | 3.400 | - | - | 129.8 | 127.0 | 2 | 7 |
| test-model | 1 | 1.000 | 0.223 | 0.953 | 0.660 | 0.333 | 0.333 | - | - | 195.0 | 157.0 | 4 | 14 |
| troubleshoot-errors | 1 | 1.000 | 0.835 | 0.965 | 0.875 | 3.000 | 2.000 | 1.000 | - | 157.2 | 122.5 | 6 | 12 |
| understand-project-structure | 1 | 1.000 | 0.525 | 4.900 | 3.083 | 0.833 | 0.167 | - | - | 171.2 | 197.2 | 14 | 16 |
| write-rich-descriptions | 1 | 1.000 | 0.417 | 9.667 | 6.200 | 0.333 | 1.667 | - | - | 111.7 | 128.7 | 2 | 7 |

## High-variance evals

No high-variance evals were flagged.

## Previous-iteration comparison

| Skill | Prev win rate | Curr win rate | Δ win rate | Prev expectation Δ | Curr expectation Δ | Δ expectation Δ | Prev time Δ / eval | Curr time Δ / eval | Δ time Δ / eval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 50.0% | 83.3% | 0.333 | 0.250 | 0.083 | -0.167 | -8.316 | -0.833 | 7.482 |
| configure-project-includes | 20.0% | 100.0% | 0.800 | 0.000 | 0.200 | 0.200 | -4.622 | 0.000 | 4.622 |
| create-element | 0.0% | 100.0% | 1.000 | 0.000 | 0.300 | 0.300 | 7.897 | -4.000 | -11.897 |
| create-relationship | 0.0% | 100.0% | 1.000 | 0.000 | 0.080 | 0.080 | -2.547 | -4.000 | -1.453 |
| create-sequence-view | 75.0% | 100.0% | 0.250 | 0.050 | 0.229 | 0.179 | 5.209 | 0.250 | -4.959 |
| customize-view | 60.0% | 80.0% | 0.200 | 0.076 | 0.430 | 0.354 | -9.235 | -1.400 | 7.835 |
| design-view | 75.0% | 100.0% | 0.250 | 0.000 | 0.562 | 0.562 | 10.164 | -0.750 | -10.914 |
| document-decision | 33.3% | 100.0% | 0.667 | 0.110 | 0.261 | 0.151 | -4.322 | -1.667 | 2.656 |
| implement-pattern | 75.0% | 100.0% | 0.250 | 0.062 | 0.312 | 0.250 | 11.953 | 0.500 | -11.453 |
| lookup-element-kinds | 40.0% | 60.0% | 0.200 | 0.000 | 0.000 | 0.000 | -1.072 | -3.800 | -2.728 |
| model-deployment-infrastructure | 25.0% | 80.0% | 0.550 | 0.000 | 0.280 | 0.280 | -12.777 | -23.800 | -11.024 |
| name-deployment-nodes | 33.3% | 100.0% | 0.667 | 0.110 | 0.917 | 0.807 | -4.117 | 0.667 | 4.783 |
| organize-multi-project | 50.0% | 100.0% | 0.500 | 0.125 | 0.250 | 0.125 | -6.632 | 1.250 | 7.882 |
| structure-deployment-tiers | 33.3% | 100.0% | 0.667 | 0.167 | 0.193 | 0.027 | -2.333 | 0.000 | 2.333 |
| sync-with-template | 0.0% | 100.0% | 1.000 | 0.000 | 0.250 | 0.250 | 7.218 | -2.400 | -9.618 |
| test-model | 66.7% | 100.0% | 0.333 | 0.110 | 0.777 | 0.667 | -0.043 | 0.000 | 0.043 |
| troubleshoot-errors | 0.0% | 100.0% | 1.000 | 0.000 | 0.165 | 0.165 | 8.750 | 1.000 | -7.750 |
| understand-project-structure | 40.0% | 100.0% | 0.600 | 0.000 | 0.475 | 0.475 | -14.561 | 0.667 | 15.227 |
| write-rich-descriptions | 33.3% | 100.0% | 0.667 | 0.167 | 0.583 | 0.417 | 2.020 | -1.333 | -3.353 |
