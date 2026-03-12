# Benchmark — c4-modeling-process

- Timestamp: 2026-03-10T19:15:00Z
- Primary configuration: `with_skill`
- Baseline: `old_skill`

| Configuration | Pass rate | Time (s) | Tokens |
|---|---:|---:|---:|
| with_skill | 100.0% ± 0.0% | - | - |
| old_skill | 88.4% ± 14.4% | - | - |

## Delta

- Pass rate: `+0.12`
- Time seconds: `-`
- Tokens: `-`

## Measurement

- Time is aggregated from the executor wall-clock duration around each `gh copilot` call.
- `timing.json` also preserves Copilot CLI `usage.totalApiDurationMs` and `usage.sessionDurationMs` when available.
- Tokens count assistant output tokens reported by the CLI JSONL stream.
- Prompt/input token counts are not currently exposed by the GitHub Copilot CLI JSONL format.

## Notes

- Primary configuration: with_skill; baseline: old_skill.
- Time metrics use executor wall-clock duration around each gh copilot subprocess; timing.json also preserves Copilot CLI totalApiDurationMs and sessionDurationMs when available.
- Token metrics use assistant output tokens from executor runs only; GitHub Copilot CLI JSONL does not expose prompt/input token counts.
- Repository-local skill leakage is reduced by isolated HOME/USERPROFILE/COPILOT_HOME per run.
- Automated grading uses an isolated `skill-creator` support workspace snapshot as methodology source of truth; that meta-skill is not exposed inside measured executor sandboxes.
- Legacy run artifacts did not persist measured time for 10 run(s) and tokens for 10 run(s); reports now show `-` instead of misleading `0` values when those metrics were unavailable.
- Les evals 0, 2 et 3 sont surtout des garde-fous : elles passent dans les deux configurations et valident le socle méthodologique commun.
- Le gain mesurable vient surtout de l’eval 1 (raisonnement explicitement C1→C2→C3 avant de décider sur C3) et de l’eval 4 (handoff net vers `model-deployment-infrastructure`).
- Chrono et tokens indisponibles : timing.json et benchmark forcés à 0. Ordre des configurations et delta normalisés.
