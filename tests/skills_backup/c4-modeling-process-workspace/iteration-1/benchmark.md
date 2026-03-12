# Benchmark — c4-modeling-process

- Timestamp: 2026-03-10T17:06:08Z
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
- Evals 0, 2 and 3 pass in both configurations; they confirm baseline competence but do not discriminate the rewrite strongly.
- The rewrite adds most of its measurable value on eval 1 (explicit C1→C2→C3 reasoning before deciding on C3) and eval 4 (clean handoff to `model-deployment-infrastructure`).
- Timing and token metrics are zero because executor metadata was not available from subagent runs in this session; compare pass rates rather than runtime costs.
- This benchmark uses 1 run per configuration, so the pass-rate delta is directional but still low-confidence until additional runs are added.
