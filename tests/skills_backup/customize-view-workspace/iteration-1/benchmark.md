# Benchmark — customize-view

- Timestamp: 2026-03-10T17:53:05Z
- Primary configuration: `with_skill`
- Baseline: `without_skill`

| Configuration | Pass rate | Time (s) | Tokens |
|---|---:|---:|---:|
| with_skill | 100.0% ± 0.0% | - | - |
| without_skill | 11.0% ± 15.6% | - | - |

## Delta

- Pass rate: `+0.89`
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
- Les baselines dérivent immédiatement vers des hex colors locaux ou des cibles `navigateTo` instables, alors que le skill maintient systématiquement palette partagée et IDs de vues existants.
- L'eval palette partagée montre une baseline partiellement utile (présence de règles `style`) mais encore insuffisante : elle échoue sur la gouvernance de palette et sur la préservation explicite du contexte.
- Le score très faible de la baseline vient surtout de deux écarts récurrents : personnalisation hors périmètre (ajouts structurels) et absence de lien/navigation stables.
- La télémétrie temps/tokens n'était pas disponible pour ces runs inline ; les métriques de temps et de tokens restent donc des placeholders à 0.
