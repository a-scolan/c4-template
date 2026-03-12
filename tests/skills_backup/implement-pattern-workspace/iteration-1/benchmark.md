# Benchmark — implement-pattern

- Timestamp: 2026-03-10T18:40:00Z
- Primary configuration: `with_skill`
- Baseline: `without_skill`

| Configuration | Pass rate | Time (s) | Tokens |
|---|---:|---:|---:|
| with_skill | 100.0% ± 0.0% | - | - |
| without_skill | 22.2% ± 15.7% | - | - |

## Delta

- Pass rate: `+0.78`
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
- Le skill transforme des conseils génériques en patrons LikeC4 concrets : kinds dédiés, relations typed et garde-fous de modélisation.
- L’intégration externe discrimine très fortement le skill : sans lui, la réponse n’invente pas naturellement `System_External`, `#External` et `-[calls]->` ensemble.
- Le baseline retrouve parfois l’idée métier (queue RabbitMQ, cache Redis), mais pas la notation typed ni les responsabilités explicites du pattern.
- La variance non nulle du baseline vient du fait que certains prompts suggèrent naturellement le composant (queue/cache) sans pour autant amener la bonne modélisation LikeC4.
