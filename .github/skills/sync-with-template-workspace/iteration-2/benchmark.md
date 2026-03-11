# Skill Benchmark: sync-with-template

**Model**: GPT-5.4
**Date**: 2026-03-10T17:53:32Z
**Evals**: 0, 1, 2 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 8% ± 14% | +0.92 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- Configuration primaire : with_skill ; baseline : without_skill.
- Les evals de workflow `sync/*` et `git subtree pull --squash` discriminent nettement le skill par rapport au baseline.
- Chrono et tokens indisponibles : timing.json et benchmark forcés à 0.