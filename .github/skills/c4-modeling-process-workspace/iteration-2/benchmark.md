# Skill Benchmark: c4-modeling-process

**Model**: GPT-5.4
**Date**: 2026-03-10T19:15:00Z
**Evals**: 0, 1, 2, 3, 4 (1 run each per configuration)

## Summary

| Metric | With Skill | Old Skill | Delta |
|--------|------------|-----------|-------|
| Pass Rate | 100% ± 0% | 88% ± 16% | +0.12 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- Configuration primaire : with_skill ; baseline : old_skill.
- Les evals 0, 2 et 3 sont surtout des garde-fous : elles passent dans les deux configurations et valident le socle méthodologique commun.
- Le gain mesurable vient surtout de l’eval 1 (raisonnement explicitement C1→C2→C3 avant de décider sur C3) et de l’eval 4 (handoff net vers `model-deployment-infrastructure`).
- Chrono et tokens indisponibles : timing.json et benchmark forcés à 0. Ordre des configurations et delta normalisés.
