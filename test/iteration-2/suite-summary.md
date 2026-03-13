# Skill Suite Summary — iteration-2

Generated at: 2026-03-13T08:20:04Z
Previous iteration: iteration-1
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

### Reading deltas

- `Expectation Δ > 0`: the skill satisfied more listed expectations.
- `Rubric Δ > 0`: the skill was judged better overall.
- `Time Δ < 0`: the skill was faster.
- `Words Δ < 0`: the skill was more concise.
- `Files read Δ > 0`: the skill consumed more repository context.

## Suite overview

All required run-metrics files were present and complete.

| Skill | Evals | With-skill win rate | Expectation Δ | Rubric Δ | Time Δ / eval (s) | Words Δ / eval | Files read Δ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 6 | 50.0% | 0.250 | 1.500 | -8.316 | -13.5 | -3.0 |
| configure-project-includes | 6 | 20.0% | 0.000 | 0.000 | -4.622 | 18.2 | -3.0 |
| create-element | 5 | 0.0% | 0.000 | -0.500 | 7.897 | -26.0 | -1.0 |
| create-relationship | 5 | 0.0% | 0.000 | -0.800 | -2.547 | -23.4 | -2.0 |
| create-sequence-view | 4 | 75.0% | 0.050 | 1.000 | 5.209 | 57.8 | -4.0 |
| customize-view | 5 | 60.0% | 0.076 | 0.600 | -9.235 | 7.4 | -3.0 |
| design-view | 4 | 75.0% | 0.000 | 0.300 | 10.164 | 89.8 | -2.0 |
| document-decision | 3 | 33.3% | 0.110 | 0.400 | -4.322 | -89.7 | 0.0 |
| implement-pattern | 4 | 75.0% | 0.062 | 1.000 | 11.953 | -49.8 | - |
| lookup-element-kinds | 5 | 40.0% | 0.000 | 0.060 | -1.072 | 71.4 | -1.0 |
| model-deployment-infrastructure | 5 | 25.0% | 0.000 | -0.250 | -12.777 | -68.0 | 1.0 |
| name-deployment-nodes | 3 | 33.3% | 0.110 | 1.000 | -4.117 | -14.7 | - |
| organize-multi-project | 4 | 50.0% | 0.125 | 1.000 | -6.632 | -6.5 | - |
| structure-deployment-tiers | 3 | 33.3% | 0.167 | 1.333 | -2.333 | 11.0 | 0.0 |
| sync-with-template | 5 | 0.0% | 0.000 | -0.375 | 7.218 | 31.5 | - |
| test-model | 3 | 66.7% | 0.110 | 1.200 | -0.043 | 98.3 | -6.0 |
| troubleshoot-errors | 4 | 0.0% | 0.000 | -0.500 | 8.750 | -29.8 | -4.0 |
| understand-project-structure | 6 | 40.0% | 0.000 | -0.040 | -14.561 | -59.8 | 1.0 |
| write-rich-descriptions | 3 | 33.3% | 0.167 | 1.667 | 2.020 | -43.3 | -1.0 |

## Per-skill detailed comparison

| Skill | Exp pass with | Exp pass without | Rubric with | Rubric without | Sec/eval with | Sec/eval without | Words/eval with | Words/eval without | Files read with | Files read without |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 1.000 | 0.750 | 9.500 | 8 | 12.600 | 20.916 | 140.7 | 154.2 | 2 | 5 |
| configure-project-includes | 1.000 | 1.000 | 8.800 | 8.800 | 16.977 | 21.600 | 128.4 | 110.2 | 3 | 6 |
| create-element | 1.000 | 1.000 | 8.500 | 9 | 22.892 | 14.995 | 78.5 | 104.5 | 4 | 5 |
| create-relationship | 1.000 | 1.000 | 8.800 | 9.600 | 14.600 | 17.147 | 93.0 | 116.4 | 2 | 4 |
| create-sequence-view | 1.000 | 0.950 | 9.250 | 8.250 | 16.240 | 11.031 | 145.8 | 88.0 | 2 | 6 |
| customize-view | 0.960 | 0.884 | 8.800 | 8.200 | 15.000 | 24.235 | 35.8 | 28.4 | 3 | 6 |
| design-view | 1.000 | 1.000 | 9.650 | 9.350 | 45.624 | 35.460 | 231.5 | 141.8 | 12 | 14 |
| document-decision | 1.000 | 0.890 | 9.200 | 8.800 | 17.849 | 22.172 | 274.0 | 363.7 | 3 | 3 |
| implement-pattern | 1.000 | 0.938 | 10 | 9 | 22.953 | 11.000 | 134.5 | 184.2 | - | 11 |
| lookup-element-kinds | 1.000 | 1.000 | 9.300 | 9.240 | 16.072 | 17.144 | 178.8 | 107.4 | 8 | 9 |
| model-deployment-infrastructure | 1.000 | 1.000 | 9.500 | 9.750 | 20.000 | 32.776 | 242.0 | 310.0 | 4 | 3 |
| name-deployment-nodes | 1.000 | 0.890 | 10 | 9 | 29.291 | 33.407 | 102.7 | 117.3 | - | 3 |
| organize-multi-project | 1.000 | 0.875 | 10 | 9 | 23.601 | 30.233 | 145.8 | 152.2 | - | 8 |
| structure-deployment-tiers | 1.000 | 0.833 | 9.333 | 8 | 33.000 | 35.333 | 252.7 | 241.7 | 4 | 4 |
| sync-with-template | 1.000 | 1.000 | 9.375 | 9.750 | 21.968 | 14.750 | 186.0 | 154.5 | - | 3 |
| test-model | 1.000 | 0.890 | 9.567 | 8.367 | 29.913 | 29.956 | 364.0 | 265.7 | 3 | 9 |
| troubleshoot-errors | 1.000 | 1.000 | 9.500 | 10 | 29.750 | 21.000 | 186.8 | 216.5 | 4 | 8 |
| understand-project-structure | 1.000 | 1.000 | 9.420 | 9.460 | 22.866 | 37.426 | 276.6 | 336.4 | 15 | 14 |
| write-rich-descriptions | 1.000 | 0.833 | 10 | 8.333 | 23.628 | 21.608 | 202.0 | 245.3 | 3 | 4 |

## Previous-iteration comparison

| Skill | Prev win rate | Curr win rate | Δ win rate | Prev expectation Δ | Curr expectation Δ | Δ expectation Δ | Prev time Δ / eval | Curr time Δ / eval | Δ time Δ / eval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| c4-modeling-process | 83.3% | 50.0% | -0.333 | 0.250 | 0.250 | 0.000 | -2.667 | -8.316 | -5.649 |
| configure-project-includes | 60.0% | 20.0% | -0.400 | 0.000 | 0.000 | 0.000 | 4.600 | -4.622 | -9.223 |
| create-element | 100.0% | 0.0% | -1.000 | 0.250 | 0.000 | -0.250 | -13.250 | 7.897 | 21.147 |
| create-relationship | 40.0% | 0.0% | -0.400 | 0.000 | 0.000 | 0.000 | 9.800 | -2.547 | -12.347 |
| create-sequence-view | 100.0% | 75.0% | -0.250 | 0.062 | 0.050 | -0.013 | -7.250 | 5.209 | 12.459 |
| customize-view | 50.0% | 60.0% | 0.100 | -0.102 | 0.076 | 0.178 | -8.750 | -9.235 | -0.485 |
| design-view | 75.0% | 75.0% | 0.000 | 0.292 | 0.000 | -0.292 | 10.250 | 10.164 | -0.086 |
| document-decision | 0.0% | 33.3% | 0.333 | 0.000 | 0.110 | 0.110 | -14.667 | -4.322 | 10.344 |
| implement-pattern | 25.0% | 75.0% | 0.500 | -0.020 | 0.062 | 0.083 | -6.500 | 11.953 | 18.453 |
| lookup-element-kinds | 40.0% | 40.0% | 0.000 | 0.000 | 0.000 | 0.000 | -18.600 | -1.072 | 17.528 |
| model-deployment-infrastructure | 75.0% | 25.0% | -0.500 | 0.145 | 0.000 | -0.145 | 2.250 | -12.777 | -15.027 |
| name-deployment-nodes | 66.7% | 33.3% | -0.333 | 0.110 | 0.110 | 0.000 | -5.667 | -4.117 | 1.550 |
| organize-multi-project | 50.0% | 50.0% | 0.000 | 0.125 | 0.125 | 0.000 | 0.250 | -6.632 | -6.882 |
| structure-deployment-tiers | 66.7% | 33.3% | -0.333 | 0.250 | 0.167 | -0.083 | -14.000 | -2.333 | 11.667 |
| sync-with-template | 75.0% | 0.0% | -0.750 | 0.000 | 0.000 | 0.000 | -12.000 | 7.218 | 19.218 |
| test-model | 100.0% | 66.7% | -0.333 | 0.417 | 0.110 | -0.307 | 7.333 | -0.043 | -7.376 |
| troubleshoot-errors | 50.0% | 0.0% | -0.500 | 0.083 | 0.000 | -0.083 | -31.750 | 8.750 | 40.500 |
| understand-project-structure | 100.0% | 40.0% | -0.600 | 0.300 | 0.000 | -0.300 | 27.600 | -14.561 | -42.161 |
| write-rich-descriptions | 100.0% | 33.3% | -0.667 | 0.167 | 0.167 | 0.000 | -24.794 | 2.020 | 26.814 |
