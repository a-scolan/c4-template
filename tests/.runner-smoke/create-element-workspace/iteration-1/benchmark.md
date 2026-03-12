# Benchmark — create-element

- Timestamp: 2026-03-12T10:55:17Z
- Primary configuration: `with_skill`
- Baseline: `without_skill`

| Configuration | Pass rate | Time (s) | Tokens |
|---|---:|---:|---:|
| with_skill | 0.0% ± 0.0% | 101.76 ± 0.00 | 3772 ± 0 |
| without_skill | 0.0% ± 0.0% | 106.78 ± 0.00 | 4046 ± 0 |

## Delta

- Pass rate: `+0.00`
- Time seconds: `-5.02`
- Tokens: `-274.00`

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
- Automated grading and benchmark analysis use an isolated `skill-creator` support workspace snapshot and read vendored agent prompts directly; that meta-skill is not exposed inside measured executor sandboxes.
- Observed 28 non-JSON output line(s); preview: ● List directory skill-creator\; └ 7 files found; ● List directory _analyzer_inputs\ (+25 more)
- MCP reinjection disabled via --no-mcp.
- The skill showed no measurable quality benefit on this benchmark: `with_skill` and `without_skill` both scored `0/3` expectations passed (`0.0` pass rate), so the run_summary delta is `+0.00` pass rate.
- All three expectations in eval `eval-la-reponse-impose-de-verifier-dabord-le-shared-s` failed in both configurations, which suggests this eval did not show any differentiating advantage from the skill in this run.
- The `with_skill` run was slightly cheaper and faster despite identical pass rate: `101.763s` vs `106.784s`, `3772` vs `4046` output tokens, and `31` vs `30` tool calls.
- The `with_skill` grading evidence points to a specific failure pattern: the answer introduced repo-specific guidance about shared specs, kinds, and permission workflow, but the grader found those claims were not grounded in the allowed local evidence.
- Benchmark reliability looks limited for this eval because grading had parsing issues in both configurations: both runs report that the primary grader did not return valid JSON, and the `with_skill` run additionally logged 11 malformed JSONL lines.
- The `without_skill` run is less diagnostic than the `with_skill` run because its failed expectations mostly say `Automated grader did not supply evidence`, whereas the `with_skill` run includes concrete evidence about unsupported claims.
