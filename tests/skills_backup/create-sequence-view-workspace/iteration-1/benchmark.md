# Benchmark — create-sequence-view

- Timestamp: 2026-03-10T17:53:04Z
- Primary configuration: `with_skill`
- Baseline: `without_skill`

| Configuration | Pass rate | Time (s) | Tokens |
|---|---:|---:|---:|
| with_skill | 100.0% ± 0.0% | - | - |
| without_skill | 33.0% ± 0.0% | - | - |

## Delta

- Pass rate: `+0.67`
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
- Legacy run artifacts did not persist measured time for 6 run(s) and tokens for 6 run(s); reports now show `-` instead of misleading `0` values when those metrics were unavailable.
- Les trois baselines gardent une partie de la forme LikeC4, mais ratent systématiquement au moins une règle centrale : mauvais type de vue, kind relationnel interdit, acteur initiateur manquant ou restriction parent→child ignorée.
- L'eval parent-child est la plus discriminante : sans le skill, la proposition conserve le lien invalide `api_container -> api_container.auth_component`, alors que la version avec skill le réécrit correctement vers l'acteur -> composant.
- Le skill ne gagne pas seulement sur la syntaxe ; il gagne aussi sur la causalité narrative, avec des labels d'action et un ordre temporel explicite sur le flux asynchrone.
- La télémétrie temps/tokens n'était pas disponible pour ces runs inline ; les métriques de temps et de tokens restent donc des placeholders à 0.
