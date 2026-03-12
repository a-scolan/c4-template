# Benchmark — write-rich-descriptions

- Timestamp: 2026-03-10T17:31:01Z
- Primary configuration: `with_skill`
- Baseline: `without_skill`

| Configuration | Pass rate | Time (s) | Tokens |
|---|---:|---:|---:|
| with_skill | 87.5% ± 12.5% | - | - |
| without_skill | 25.0% ± 0.0% | - | - |

## Delta

- Pass rate: `+0.62`
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
- Legacy run artifacts did not persist measured time for 4 run(s) and tokens for 4 run(s); reports now show `-` instead of misleading `0` values when those metrics were unavailable.
- L'eval de prérequis révèle un point faible réel : le handoff cite `model-deployment` au lieu du vrai skill `model-deployment-infrastructure`.
- En revanche, le skill reste fort sur l'ordre des infos ops (`eth0` d'abord, gateway côté zone, metadata optionnelle).
- Les métriques temps/tokens valent 0 ici faute de métadonnées d'exécution récupérables dans cette session ; compare surtout les pass rates.
- Cette itération n'a qu'1 run par configuration : la tendance est utile, mais encore peu robuste statistiquement.
