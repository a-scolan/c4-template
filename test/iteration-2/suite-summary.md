# Skill Suite Summary — iteration-2

Generated at: 2026-03-26T16:09:43Z
Previous iteration: iteration-1
Protocol version: benchmark-v3
Skill count: 20

## Metric validation

Status: passed
Files checked: 40/40
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
| With-skill win rate | 0.684 | 0.210 | 0.200 | 1.000 |
| Expectation Δ | 0.217 | 0.150 | -0.040 | 0.456 |
| Rubric Δ | 1.535 | 0.936 | -0.120 | 3.000 |
| Time Δ / eval | -4.700 | 18.067 | -47.222 | 20.567 |
| Executable Δ | 0.196 | 0.615 | -1.000 | 1.000 |


## Suite overview

All required run-metrics files were present and complete.

| Skill | Evals | Runs | With-skill win rate | Expectation Δ | Rubric Δ | Time Δ / eval (s) | Executable Δ | Words Δ / eval | Files read Δ | High-var evals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 6 | 3 | 50.0% | 0.097 | 0.700 | -6.278 | - | -32.7 | 2.0 | 4 |
| configure-project-includes | 6 | 3 | 83.3% | 0.275 | 2.133 | -9.722 | 0.333 | 60.8 | -0.3 | 6 |
| create-element | 5 | 3 | 100.0% | 0.220 | 2.000 | 7.733 | 0.444 | 82.7 | 2.7 | 0 |
| create-relationship | 5 | 3 | 60.0% | -0.040 | 0.360 | -10.000 | -0.200 | 130.3 | 0.0 | 5 |
| create-sequence-view | 4 | 3 | 75.0% | 0.354 | 1.250 | -12.500 | -1.000 | 176.0 | 0.0 | 5 |
| customize-view | 5 | 3 | 80.0% | 0.243 | 1.520 | -10.000 | 1.000 | 141.7 | 0.0 | 2 |
| design-view | 4 | 3 | 50.0% | 0.438 | 3.000 | 9.500 | 0.083 | -206.4 | 1.0 | 1 |
| document-decision | 3 | 3 | 100.0% | 0.456 | 2.267 | 0.000 | - | -16.0 | 0.0 | 5 |
| implement-pattern | 4 | 3 | 75.0% | 0.000 | 2.825 | -12.500 | 1.000 | -226.2 | 0.0 | 4 |
| likec4-dsl | 21 | 3 | 76.2% | 0.267 | 2.381 | -0.667 | 0.000 | 0.6 | 1.0 | 0 |
| lookup-element-kinds | 5 | 3 | 20.0% | 0.000 | -0.120 | 0.000 | 0.100 | -156.9 | 0.0 | 7 |
| model-deployment-infrastructure | 5 | 3 | 60.0% | 0.200 | 1.800 | -10.000 | - | -183.0 | 0.0 | 5 |
| name-deployment-nodes | 3 | 3 | 66.7% | 0.278 | 1.700 | -16.667 | - | -233.4 | 0.0 | 6 |
| organize-multi-project | 4 | 3 | 50.0% | 0.188 | 0.325 | 16.500 | - | -257.0 | -2.0 | 6 |
| structure-deployment-tiers | 3 | 3 | 33.3% | 0.110 | 0.433 | 20.567 | - | -101.0 | -5.0 | 5 |
| sync-with-template | 5 | 3 | 80.0% | 0.150 | 1.200 | -46.000 | - | -67.0 | 0.0 | 3 |
| test-model | 3 | 3 | 66.7% | 0.028 | 0.300 | -47.222 | - | -59.6 | 1.0 | 3 |
| troubleshoot-errors | 4 | 3 | 75.0% | 0.355 | 2.125 | 7.250 | - | -22.8 | 1.0 | 0 |
| understand-project-structure | 6 | 3 | 100.0% | 0.308 | 2.667 | 8.667 | - | 35.0 | 1.0 | 0 |
| write-rich-descriptions | 3 | 3 | 66.7% | 0.417 | 1.833 | 17.333 | - | 1.0 | 0.7 | 2 |

## Per-skill detailed comparison

| Skill | Runs | Exp pass with | Exp pass without | Rubric with | Rubric without | Sec/eval with | Sec/eval without | Exec with | Exec without | Words/eval with | Words/eval without | Files read with | Files read without |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 3 | 1.000 | 0.903 | 9.233 | 8.533 | 3.000 | 9.278 | 1.000 | - | 90.7 | 123.3 | 2.0 | 0.0 |
| configure-project-includes | 3 | 0.967 | 0.692 | 9.467 | 7.333 | 10.278 | 20.000 | 0.333 | 0.000 | 216.0 | 155.2 | 0.7 | 1.0 |
| create-element | 3 | 0.910 | 0.690 | 9.080 | 7.080 | 21.733 | 14.000 | 1.000 | 0.556 | 134.4 | 51.7 | 3.7 | 1.0 |
| create-relationship | 3 | 0.880 | 0.920 | 8.820 | 8.460 | 14.000 | 24.000 | 0.800 | 1.000 | 161.2 | 30.9 | 1.0 | 1.0 |
| create-sequence-view | 3 | 0.938 | 0.583 | 8.500 | 7.250 | 17.500 | 30.000 | 0.000 | 1.000 | 234.8 | 58.8 | 1.0 | 1.0 |
| customize-view | 3 | 0.880 | 0.637 | 8.660 | 7.140 | 14.000 | 24.000 | 1.000 | 0.000 | 160.8 | 19.1 | 1.0 | 1.0 |
| design-view | 3 | 0.500 | 0.062 | 6.250 | 3.250 | 17.500 | 8.000 | 0.750 | 0.667 | 104.5 | 310.9 | 1.0 | 0.0 |
| document-decision | 3 | 1.000 | 0.544 | 9.100 | 6.833 | 23.333 | 23.333 | - | - | 252.8 | 268.8 | 1.0 | 1.0 |
| implement-pattern | 3 | 0.855 | 0.855 | 7.825 | 5.000 | 17.500 | 30.000 | 1.000 | 0.000 | 114.5 | 340.8 | 1.0 | 1.0 |
| likec4-dsl | 3 | 0.981 | 0.714 | 8.857 | 6.476 | 3.333 | 4.000 | 0.625 | 0.625 | 40.5 | 39.9 | 1.0 | 0.0 |
| lookup-element-kinds | 3 | 1.000 | 1.000 | 9.480 | 9.600 | 14.000 | 14.000 | 1.000 | 0.900 | 74.0 | 230.9 | 1.0 | 1.0 |
| model-deployment-infrastructure | 3 | 0.910 | 0.710 | 9.200 | 7.400 | 14.000 | 24.000 | - | 0.867 | 89.8 | 272.8 | 1.0 | 1.0 |
| name-deployment-nodes | 3 | 0.667 | 0.389 | 7.433 | 5.733 | 23.333 | 40.000 | 1.000 | - | 141.8 | 375.2 | 1.0 | 1.0 |
| organize-multi-project | 3 | 0.875 | 0.688 | 8.725 | 8.400 | 17.500 | 1.000 | - | - | 110.5 | 367.5 | 1.0 | 3.0 |
| structure-deployment-tiers | 3 | 0.917 | 0.807 | 9.067 | 8.633 | 23.333 | 2.767 | 0.000 | - | 209.1 | 310.1 | 1.0 | 6.0 |
| sync-with-template | 3 | 0.910 | 0.760 | 9.200 | 8 | 14.000 | 60.000 | - | - | 76.7 | 143.7 | 1.0 | 1.0 |
| test-model | 3 | 0.500 | 0.472 | 8.100 | 7.800 | 23.333 | 70.556 | - | - | 179.8 | 239.3 | 1.0 | 0.0 |
| troubleshoot-errors | 3 | 0.917 | 0.562 | 8.600 | 6.475 | 17.500 | 10.250 | 0.500 | - | 106.5 | 129.2 | 1.0 | 0.0 |
| understand-project-structure | 3 | 0.967 | 0.658 | 9.667 | 7 | 11.667 | 3.000 | - | - | 138.7 | 103.7 | 1.0 | 0.0 |
| write-rich-descriptions | 3 | 0.750 | 0.333 | 7.933 | 6.100 | 23.333 | 6.000 | - | - | 108.3 | 107.3 | 1.0 | 0.3 |

## High-variance evals

| Skill | Source | Eval | Run count | Winner flips | Expectation stddev | Rubric stddev |
| --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | without_skill | 0 | - | no | - | - |
| c4-modeling-process | without_skill | 3 | - | no | - | - |
| c4-modeling-process | without_skill | 4 | - | no | - | - |
| c4-modeling-process | without_skill | 5 | - | no | - | - |
| configure-project-includes | without_skill | 0 | - | no | - | - |
| configure-project-includes | without_skill | 1 | - | no | - | - |
| configure-project-includes | without_skill | 2 | - | no | - | - |
| configure-project-includes | without_skill | 3 | - | no | - | - |
| configure-project-includes | without_skill | 4 | - | no | - | - |
| configure-project-includes | without_skill | 5 | - | no | - | - |
| create-relationship | without_skill | 0 | - | no | - | - |
| create-relationship | without_skill | 1 | - | no | - | - |
| create-relationship | without_skill | 2 | - | no | - | - |
| create-relationship | without_skill | 3 | - | no | - | - |
| create-relationship | without_skill | 4 | - | no | - | - |
| create-sequence-view | with_skill | 0 | - | no | - | - |
| create-sequence-view | without_skill | 0 | - | no | - | - |
| create-sequence-view | without_skill | 1 | - | no | - | - |
| create-sequence-view | without_skill | 2 | - | no | - | - |
| create-sequence-view | without_skill | 3 | - | no | - | - |
| customize-view | with_skill | 2 | - | no | - | - |
| customize-view | without_skill | 3 | - | no | - | - |
| design-view | without_skill | 0 | - | no | - | - |
| document-decision | with_skill | 0 | - | no | - | - |
| document-decision | with_skill | 1 | - | no | - | - |
| document-decision | with_skill | 2 | - | no | - | - |
| document-decision | without_skill | 1 | - | no | - | - |
| document-decision | without_skill | 2 | - | no | - | - |
| implement-pattern | without_skill | 0 | - | no | - | - |
| implement-pattern | without_skill | 1 | - | no | - | - |
| implement-pattern | without_skill | 2 | - | no | - | - |
| implement-pattern | without_skill | 3 | - | no | - | - |
| lookup-element-kinds | with_skill | 0 | - | no | - | - |
| lookup-element-kinds | with_skill | 3 | - | no | - | - |
| lookup-element-kinds | without_skill | 0 | - | no | - | - |
| lookup-element-kinds | without_skill | 1 | - | no | - | - |
| lookup-element-kinds | without_skill | 2 | - | no | - | - |
| lookup-element-kinds | without_skill | 3 | - | no | - | - |
| lookup-element-kinds | without_skill | 4 | - | no | - | - |
| model-deployment-infrastructure | without_skill | 0 | - | no | - | - |
| model-deployment-infrastructure | without_skill | 1 | - | no | - | - |
| model-deployment-infrastructure | without_skill | 2 | - | no | - | - |
| model-deployment-infrastructure | without_skill | 3 | - | no | - | - |
| model-deployment-infrastructure | without_skill | 4 | - | no | - | - |
| name-deployment-nodes | with_skill | 0 | - | no | - | - |
| name-deployment-nodes | with_skill | 1 | - | no | - | - |
| name-deployment-nodes | with_skill | 2 | - | no | - | - |
| name-deployment-nodes | without_skill | 0 | - | no | - | - |
| name-deployment-nodes | without_skill | 1 | - | no | - | - |
| name-deployment-nodes | without_skill | 2 | - | no | - | - |
| organize-multi-project | with_skill | 0 | - | no | - | - |
| organize-multi-project | with_skill | 3 | - | no | - | - |
| organize-multi-project | without_skill | 0 | - | no | - | - |
| organize-multi-project | without_skill | 1 | - | no | - | - |
| organize-multi-project | without_skill | 2 | - | no | - | - |
| organize-multi-project | without_skill | 3 | - | no | - | - |
| structure-deployment-tiers | with_skill | 0 | - | no | - | - |
| structure-deployment-tiers | with_skill | 2 | - | no | - | - |
| structure-deployment-tiers | without_skill | 0 | - | no | - | - |
| structure-deployment-tiers | without_skill | 1 | - | no | - | - |
| structure-deployment-tiers | without_skill | 2 | - | no | - | - |
| sync-with-template | with_skill | 0 | - | no | - | - |
| sync-with-template | with_skill | 4 | - | no | - | - |
| sync-with-template | without_skill | 0 | - | no | - | - |
| test-model | with_skill | 0 | - | no | - | - |
| test-model | with_skill | 1 | - | no | - | - |
| test-model | with_skill | 2 | - | no | - | - |
| write-rich-descriptions | with_skill | 0 | - | no | - | - |
| write-rich-descriptions | with_skill | 2 | - | no | - | - |

## Previous-iteration comparison

| Skill | Prev win rate | Curr win rate | Δ win rate | Prev expectation Δ | Curr expectation Δ | Δ expectation Δ | Prev time Δ / eval | Curr time Δ / eval | Δ time Δ / eval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 83.3% | 50.0% | -0.333 | 0.097 | 0.097 | -0.001 | -7.333 | -6.278 | 1.056 |
| configure-project-includes | 83.3% | 83.3% | 0.000 | 0.200 | 0.275 | 0.075 | -10.667 | -9.722 | 0.945 |
| create-element | 80.0% | 100.0% | 0.200 | 0.230 | 0.220 | -0.010 | -33.600 | 7.733 | 41.333 |
| create-relationship | 60.0% | 60.0% | 0.000 | 0.200 | -0.040 | -0.240 | -12.800 | -10.000 | 2.800 |
| create-sequence-view | 100.0% | 75.0% | -0.250 | 0.312 | 0.354 | 0.042 | -3.500 | -12.500 | -9.000 |
| customize-view | 100.0% | 80.0% | -0.200 | 0.247 | 0.243 | -0.003 | -31.800 | -10.000 | 21.800 |
| design-view | 75.0% | 50.0% | -0.250 | 0.417 | 0.438 | 0.021 | -11.750 | 9.500 | 21.250 |
| document-decision | 100.0% | 100.0% | 0.000 | 0.150 | 0.456 | 0.306 | 0.333 | 0.000 | -0.333 |
| implement-pattern | 100.0% | 75.0% | -0.250 | 0.312 | 0.000 | -0.312 | -0.250 | -12.500 | -12.250 |
| lookup-element-kinds | 100.0% | 20.0% | -0.800 | 0.400 | 0.000 | -0.400 | -16.600 | 0.000 | 16.600 |
| model-deployment-infrastructure | 100.0% | 60.0% | -0.400 | 0.230 | 0.200 | -0.030 | -0.800 | -10.000 | -9.200 |
| name-deployment-nodes | 100.0% | 66.7% | -0.333 | 0.445 | 0.278 | -0.167 | 25.667 | -16.667 | -42.333 |
| organize-multi-project | 100.0% | 50.0% | -0.500 | 0.250 | 0.188 | -0.062 | -9.000 | 16.500 | 25.500 |
| structure-deployment-tiers | 100.0% | 33.3% | -0.667 | 0.111 | 0.110 | -0.001 | 198.667 | 20.567 | -178.100 |
| sync-with-template | 80.0% | 80.0% | 0.000 | 0.240 | 0.150 | -0.090 | -16.000 | -46.000 | -30.000 |
| test-model | 33.3% | 66.7% | 0.333 | 0.028 | 0.028 | 0.000 | 3.333 | -47.222 | -50.556 |
| troubleshoot-errors | 75.0% | 75.0% | 0.000 | 0.083 | 0.355 | 0.272 | -14.250 | 7.250 | 21.500 |
| understand-project-structure | 83.3% | 100.0% | 0.167 | 0.100 | 0.308 | 0.208 | -10.000 | 8.667 | 18.667 |
| write-rich-descriptions | 100.0% | 66.7% | -0.333 | 0.667 | 0.417 | -0.250 | -15.000 | 17.333 | 32.333 |
