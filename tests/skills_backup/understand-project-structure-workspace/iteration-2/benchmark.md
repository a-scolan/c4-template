# Benchmark — understand-project-structure

- Timestamp: 2026-03-10T19:05:00Z
- Primary configuration: `with_skill`
- Baseline: `without_skill`

| Configuration | Pass rate | Time (s) | Tokens |
|---|---:|---:|---:|
| with_skill | 100.0% ± 0.0% | - | - |
| without_skill | 43.8% ± 10.8% | - | - |

## Delta

- Pass rate: `+0.56`
- Time seconds: `-`
- Tokens: `-`

## Measurement

- Time is aggregated from the executor wall-clock duration around each `gh copilot` call.
- `timing.json` also preserves Copilot CLI `usage.totalApiDurationMs` and `usage.sessionDurationMs` when available.
- Tokens count assistant output tokens reported by the CLI JSONL stream.
- Prompt/input token counts are not currently exposed by the GitHub Copilot CLI JSONL format.

## Notes

- Primary configuration: with_skill; baseline: without_skill.
- Time metrics use executor wall-clock duration around each gh copilot subprocess; timing.json also preserves Copilot CLI totalApiDurationMs and sessionDurationMs when available.
- Token metrics use assistant output tokens from executor runs only; GitHub Copilot CLI JSONL does not expose prompt/input token counts.
- Repository-local skill leakage is reduced by isolated HOME/USERPROFILE/COPILOT_HOME per run.
- Automated grading uses an isolated `skill-creator` support workspace snapshot as methodology source of truth; that meta-skill is not exposed inside measured executor sandboxes.
- Legacy run artifacts did not persist measured time for 8 run(s) and tokens for 8 run(s); reports now show `-` instead of misleading `0` values when those metrics were unavailable.
- Cette itération couvre les 4 evals, y compris le handoff vers `c4-modeling-process`, et remplace le faux baseline précédent par un vrai `without_skill`.
- Le skill discrimine surtout sur la rigueur de recadrage multi-projet : `list-projects`, `read-project-summary`, specs partagées et taxonomie valide avant édition.
- Chrono et tokens indisponibles : timing.json et benchmark forcés à 0. Ordre des configurations et delta normalisés.
