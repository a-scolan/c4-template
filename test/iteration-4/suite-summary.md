# Skill Suite Summary — iteration-4

Generated at: 2026-03-16T16:36:40Z
Previous iteration: iteration-3
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
| With-skill win rate | 0.558 | 0.387 | 0.000 | 1.000 |
| Expectation Δ | 0.108 | 0.299 | -0.400 | 0.667 |
| Rubric Δ | 0.406 | 2.268 | -4.000 | 4.667 |
| Time Δ / eval | -6.417 | 13.198 | -30.013 | 17.616 |
| Executable Δ | 0.333 | 0.577 | 0.000 | 1.000 |


## Suite overview

All required run-metrics files were present and complete.

| Skill | Evals | Runs | With-skill win rate | Expectation Δ | Rubric Δ | Time Δ / eval (s) | Executable Δ | Words Δ / eval | Files read Δ | High-var evals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 6 | 1 | 83.3% | 0.361 | 1.667 | -8.604 | - | -2.3 | -4.0 | 0 |
| configure-project-includes | 6 | 1 | 66.7% | 0.058 | 0.833 | -5.940 | - | -22.2 | -5.0 | 0 |
| create-element | 5 | 1 | 80.0% | 0.090 | 1.200 | 6.040 | - | -1.2 | 2.0 | 0 |
| create-relationship | 5 | 1 | 0.0% | -0.400 | -4.000 | 2.961 | 1.000 | -13.2 | 1.0 | 0 |
| create-sequence-view | 4 | 1 | 0.0% | -0.354 | -3.500 | -5.245 | - | -43.5 | -1.0 | 0 |
| customize-view | 5 | 1 | 100.0% | 0.400 | 2.800 | -21.683 | 0.000 | 7.4 | -5.0 | 0 |
| design-view | 4 | 1 | 50.0% | 0.250 | 1.000 | 10.613 | - | -106.5 | -1.0 | 0 |
| document-decision | 3 | 1 | 66.7% | 0.039 | 0.333 | 17.616 | - | -22.0 | 2.0 | 0 |
| implement-pattern | 4 | 1 | 25.0% | -0.167 | -1.750 | -11.473 | 0.000 | -15.5 | -3.0 | 0 |
| lookup-element-kinds | 5 | 1 | 0.0% | -0.300 | -2.400 | 7.321 | - | -31.6 | 1.0 | 0 |
| model-deployment-infrastructure | 5 | 1 | 40.0% | 0.210 | 0.840 | 4.142 | - | -19.4 | -1.0 | 0 |
| name-deployment-nodes | 3 | 1 | 100.0% | 0.667 | 4.667 | -29.915 | - | -15.7 | -1.0 | 0 |
| organize-multi-project | 4 | 1 | 100.0% | 0.188 | 1.000 | -3.463 | - | -23.8 | -2.0 | 0 |
| structure-deployment-tiers | 3 | 1 | 0.0% | -0.111 | -1.433 | -7.848 | - | -50.3 | 0.0 | 0 |
| sync-with-template | 5 | 1 | 40.0% | 0.030 | 0.200 | -5.514 | - | -50.6 | -1.0 | 0 |
| test-model | 3 | 1 | 100.0% | 0.222 | 1.333 | -30.013 | - | 44.0 | -4.0 | 0 |
| troubleshoot-errors | 4 | 1 | 25.0% | 0.021 | -0.250 | -22.573 | - | -13.0 | -3.0 | 0 |
| understand-project-structure | 6 | 1 | 83.3% | 0.175 | 1.167 | -3.585 | - | -32.0 | 1.0 | 0 |
| write-rich-descriptions | 3 | 1 | 100.0% | 0.667 | 4.000 | -14.763 | - | 3.7 | -2.0 | 0 |

## Per-skill detailed comparison

| Skill | Runs | Exp pass with | Exp pass without | Rubric with | Rubric without | Sec/eval with | Sec/eval without | Exec with | Exec without | Words/eval with | Words/eval without | Files read with | Files read without |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 1 | 1.000 | 0.639 | 8.833 | 7.167 | 0.979 | 9.582 | - | - | 80.2 | 82.5 | 2.0 | 6.0 |
| configure-project-includes | 1 | 0.858 | 0.800 | 8.333 | 7.500 | 2.021 | 7.960 | - | - | 59.2 | 81.3 | 2.0 | 7.0 |
| create-element | 1 | 0.830 | 0.740 | 8.200 | 7 | 9.506 | 3.466 | - | 1.000 | 53.4 | 54.6 | 7.0 | 5.0 |
| create-relationship | 1 | 0.520 | 0.920 | 5 | 9 | 8.408 | 5.447 | 1.000 | 0.000 | 52.0 | 65.2 | 2.0 | 1.0 |
| create-sequence-view | 1 | 0.396 | 0.750 | 4.750 | 8.250 | 2.290 | 7.535 | - | 0.000 | 55.0 | 98.5 | 2.0 | 3.0 |
| customize-view | 1 | 0.840 | 0.440 | 8.200 | 5.400 | 0.974 | 22.657 | 0.000 | 0.000 | 28.4 | 21.0 | 2.0 | 7.0 |
| design-view | 1 | 0.625 | 0.375 | 7 | 6 | 14.671 | 4.058 | - | 0.500 | 66.5 | 173.0 | 4.0 | 5.0 |
| document-decision | 1 | 0.889 | 0.850 | 8.667 | 8.333 | 22.394 | 4.778 | - | - | 115.7 | 137.7 | 2.0 | 0.0 |
| implement-pattern | 1 | 0.542 | 0.708 | 6.250 | 8 | 0.005 | 11.479 | 1.000 | 1.000 | 60.8 | 76.2 | 2.0 | 5.0 |
| lookup-element-kinds | 1 | 0.700 | 1.000 | 6.600 | 9 | 11.444 | 4.122 | - | - | 53.2 | 84.8 | 8.0 | 7.0 |
| model-deployment-infrastructure | 1 | 0.920 | 0.710 | 8.960 | 8.120 | 12.698 | 8.557 | - | 0.000 | 92.0 | 111.4 | 3.0 | 4.0 |
| name-deployment-nodes | 1 | 0.917 | 0.250 | 8.667 | 4 | 0.016 | 29.932 | - | - | 65.0 | 80.7 | 2.0 | 3.0 |
| organize-multi-project | 1 | 0.812 | 0.625 | 8.750 | 7.750 | 1.111 | 4.574 | - | - | 86.5 | 110.2 | 2.0 | 4.0 |
| structure-deployment-tiers | 1 | 0.694 | 0.806 | 7.200 | 8.633 | 5.214 | 13.062 | - | - | 86.3 | 136.7 | 2.0 | 2.0 |
| sync-with-template | 1 | 0.790 | 0.760 | 8 | 7.800 | 0.762 | 6.276 | - | - | 59.2 | 109.8 | 2.0 | 3.0 |
| test-model | 1 | 0.500 | 0.278 | 7.333 | 6 | 0.006 | 30.020 | - | - | 196.0 | 152.0 | 2.0 | 6.0 |
| troubleshoot-errors | 1 | 0.854 | 0.833 | 8 | 8.250 | 2.634 | 25.206 | - | - | 99.5 | 112.5 | 2.0 | 5.0 |
| understand-project-structure | 1 | 0.867 | 0.692 | 8.167 | 7 | 5.493 | 9.079 | - | - | 87.8 | 119.8 | 8.0 | 7.0 |
| write-rich-descriptions | 1 | 0.750 | 0.083 | 8.333 | 4.333 | 1.499 | 16.262 | - | - | 106.7 | 103.0 | 2.0 | 4.0 |

## High-variance evals

No high-variance evals were flagged.

## Previous-iteration comparison

| Skill | Prev win rate | Curr win rate | Δ win rate | Prev expectation Δ | Curr expectation Δ | Δ expectation Δ | Prev time Δ / eval | Curr time Δ / eval | Δ time Δ / eval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 83.3% | 83.3% | 0.000 | 0.083 | 0.361 | 0.278 | -0.833 | -8.604 | -7.771 |
| configure-project-includes | 100.0% | 66.7% | -0.333 | 0.200 | 0.058 | -0.142 | 0.000 | -5.940 | -5.940 |
| create-element | 100.0% | 80.0% | -0.200 | 0.300 | 0.090 | -0.210 | -4.000 | 6.040 | 10.040 |
| create-relationship | 100.0% | 0.0% | -1.000 | 0.080 | -0.400 | -0.480 | -4.000 | 2.961 | 6.961 |
| create-sequence-view | 100.0% | 0.0% | -1.000 | 0.229 | -0.354 | -0.583 | 0.250 | -5.245 | -5.495 |
| customize-view | 80.0% | 100.0% | 0.200 | 0.430 | 0.400 | -0.030 | -1.400 | -21.683 | -20.283 |
| design-view | 100.0% | 50.0% | -0.500 | 0.562 | 0.250 | -0.312 | -0.750 | 10.613 | 11.363 |
| document-decision | 100.0% | 66.7% | -0.333 | 0.261 | 0.039 | -0.222 | -1.667 | 17.616 | 19.283 |
| implement-pattern | 100.0% | 25.0% | -0.750 | 0.312 | -0.167 | -0.479 | 0.500 | -11.473 | -11.973 |
| lookup-element-kinds | 60.0% | 0.0% | -0.600 | 0.000 | -0.300 | -0.300 | -3.800 | 7.321 | 11.121 |
| model-deployment-infrastructure | 80.0% | 40.0% | -0.400 | 0.280 | 0.210 | -0.070 | -23.800 | 4.142 | 27.942 |
| name-deployment-nodes | 100.0% | 100.0% | 0.000 | 0.917 | 0.667 | -0.250 | 0.667 | -29.915 | -30.582 |
| organize-multi-project | 100.0% | 100.0% | 0.000 | 0.250 | 0.188 | -0.062 | 1.250 | -3.463 | -4.713 |
| structure-deployment-tiers | 100.0% | 0.0% | -1.000 | 0.193 | -0.111 | -0.304 | 0.000 | -7.848 | -7.848 |
| sync-with-template | 100.0% | 40.0% | -0.600 | 0.250 | 0.030 | -0.220 | -2.400 | -5.514 | -3.114 |
| test-model | 100.0% | 100.0% | 0.000 | 0.777 | 0.222 | -0.554 | 0.000 | -30.013 | -30.013 |
| troubleshoot-errors | 100.0% | 25.0% | -0.750 | 0.165 | 0.021 | -0.144 | 1.000 | -22.573 | -23.573 |
| understand-project-structure | 100.0% | 83.3% | -0.167 | 0.475 | 0.175 | -0.300 | 0.667 | -3.585 | -4.252 |
| write-rich-descriptions | 100.0% | 100.0% | 0.000 | 0.583 | 0.667 | 0.083 | -1.333 | -14.763 | -13.430 |
