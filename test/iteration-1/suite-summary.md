# Skill Suite Summary — iteration-1

Generated at: 2026-03-12T15:17:30Z
Previous iteration: None found
Skill count: 19

## Metric legend

| Metric | Meaning | How to read it |
| --- | --- | --- |
| With-skill win rate | Share of blind comparisons won by the `with_skill` response. | Higher is better for the skill. Ties are not wins. |
| Expectation pass rate | Average share of listed expectations satisfied by a response. | Higher is better. `Expectation Δ = with_skill - without_skill`. |
| Rubric score | Blind comparator overall quality score on a 0-10 scale. | Higher is better. `Rubric Δ = with_skill - without_skill`. |
| Time per eval | Average wall-clock seconds spent per eval. | Lower is faster. `Time Δ = with_skill - without_skill`, so a negative delta means the skill was faster. |
| Words per eval | Average response length in words. | Lower means more concise, but not automatically better unless quality stays strong. |
| Files read count | Count of repository files intentionally read during a run. | Proxy for context consumption. Higher means more repository context was consumed. |

### Reading deltas

- `Expectation Δ > 0`: the skill satisfied more listed expectations.
- `Rubric Δ > 0`: the skill was judged better overall.
- `Time Δ < 0`: the skill was faster.
- `Words Δ < 0`: the skill was more concise.
- `Files read Δ > 0`: the skill consumed more repository context.

## Suite overview

| Skill | Evals | With-skill win rate | Expectation Δ | Rubric Δ | Time Δ / eval (s) | Words Δ / eval | Files read Δ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 6 | 83.3% | 0.250 | 1.517 | -2.667 | -19.2 | 1 |
| configure-project-includes | 5 | 60.0% | 0.000 | 0.420 | 4.600 | -8.4 | 0 |
| create-element | 4 | 100.0% | 0.250 | 1.625 | -13.250 | 4.8 | 1 |
| create-relationship | 5 | 40.0% | 0.000 | -0.020 | 9.800 | -7.2 | 1 |
| create-sequence-view | 4 | 100.0% | 0.062 | 0.925 | -7.250 | -21.0 | 0 |
| customize-view | 4 | 50.0% | -0.102 | -0.975 | -8.750 | -1.2 | 0 |
| design-view | 4 | 75.0% | 0.292 | 1.500 | 10.250 | 40.8 | -1 |
| document-decision | 3 | 0.0% | 0.000 | -0.533 | -14.667 | -121.3 | 0 |
| implement-pattern | 4 | 25.0% | -0.020 | -0.600 | -6.500 | -27.0 | 0 |
| lookup-element-kinds | 5 | 40.0% | 0.000 | -0.140 | -18.600 | 6.2 | 0 |
| model-deployment-infrastructure | 4 | 75.0% | 0.145 | 0.575 | 2.250 | 60.5 | 2 |
| name-deployment-nodes | 3 | 66.7% | 0.110 | 0.900 | -5.667 | 12.3 | 0 |
| organize-multi-project | 4 | 50.0% | 0.125 | 0.350 | 0.250 | -0.8 | 0 |
| structure-deployment-tiers | 3 | 66.7% | 0.250 | 0.833 | -14.000 | -49.3 | 3.0 |
| sync-with-template | 4 | 75.0% | 0.000 | 0.125 | -12.000 | 34.0 | 1 |
| test-model | 3 | 100.0% | 0.417 | 1.433 | 7.333 | -74.0 | 2 |
| troubleshoot-errors | 4 | 50.0% | 0.083 | 0.125 | -31.750 | -15.5 | 1 |
| understand-project-structure | 5 | 100.0% | 0.300 | 2.140 | 27.600 | 84.2 | 3 |
| write-rich-descriptions | 3 | 100.0% | 0.167 | 1.300 | -24.794 | -40.3 | -1 |

## Per-skill detailed comparison

| Skill | Exp pass with | Exp pass without | Rubric with | Rubric without | Sec/eval with | Sec/eval without | Words/eval with | Words/eval without | Files read with | Files read without |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 1.000 | 0.750 | 9.450 | 7.933 | 12.833 | 15.500 | 117.5 | 136.7 | 2 | 1 |
| configure-project-includes | 0.950 | 0.950 | 9.340 | 8.920 | 21.600 | 17.000 | 144.0 | 152.4 | 3 | 3 |
| create-element | 1.000 | 0.750 | 9.500 | 7.875 | 7.500 | 20.750 | 72.2 | 67.5 | 5 | 4 |
| create-relationship | 1.000 | 1.000 | 9.460 | 9.480 | 24.000 | 14.200 | 76.0 | 83.2 | 4 | 3 |
| create-sequence-view | 1.000 | 0.938 | 9.400 | 8.475 | 35.250 | 42.500 | 97.5 | 118.5 | 7 | 7 |
| customize-view | 0.835 | 0.938 | 7.725 | 8.700 | 34.250 | 43.000 | 31.5 | 32.8 | 3 | 3 |
| design-view | 1.000 | 0.708 | 9.250 | 7.750 | 39.500 | 29.250 | 144.0 | 103.2 | 4 | 5 |
| document-decision | 1.000 | 1.000 | 9.000 | 9.533 | 26.333 | 41.000 | 176.7 | 298.0 | 2 | 2 |
| implement-pattern | 0.917 | 0.938 | 8.650 | 9.250 | 18.500 | 25.000 | 90.0 | 117.0 | 2 | 2 |
| lookup-element-kinds | 1.000 | 1.000 | 9.140 | 9.280 | 30.800 | 49.400 | 120.2 | 114.0 | 5 | 5 |
| model-deployment-infrastructure | 1.000 | 0.855 | 9.275 | 8.700 | 33.750 | 31.500 | 264.8 | 204.2 | 4 | 2 |
| name-deployment-nodes | 1.000 | 0.890 | 9.200 | 8.300 | 34.667 | 40.333 | 100.3 | 88.0 | 2 | 2 |
| organize-multi-project | 1.000 | 0.875 | 9.125 | 8.775 | 31.500 | 31.250 | 137.2 | 138.0 | 5 | 5 |
| structure-deployment-tiers | 1.000 | 0.750 | 9.200 | 8.367 | 18.667 | 32.667 | 254.3 | 303.7 | 3 | 0 |
| sync-with-template | 1.000 | 1.000 | 9.425 | 9.300 | 18.250 | 30.250 | 173.8 | 139.8 | 2 | 1 |
| test-model | 1.000 | 0.583 | 9.167 | 7.733 | 56.000 | 48.667 | 257.3 | 331.3 | 4 | 2 |
| troubleshoot-errors | 1.000 | 0.917 | 9.450 | 9.325 | 17.250 | 49.000 | 188.8 | 204.2 | 7 | 6 |
| understand-project-structure | 1.000 | 0.700 | 9.500 | 7.360 | 47.600 | 20.000 | 400.4 | 316.2 | 14 | 11 |
| write-rich-descriptions | 1.000 | 0.833 | 9.367 | 8.067 | 33.333 | 58.128 | 205.0 | 245.3 | 2 | 3 |

## Previous-iteration comparison

No previous iteration was found for comparison.
