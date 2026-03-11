# Skill Benchmark: understand-project-structure

**Model**: GPT-5.4
**Date**: 2026-03-10T19:05:00Z
**Evals**: 0, 1, 2, 3 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 44% ± 13% | +0.56 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- Configuration primaire : with_skill ; baseline : without_skill.
- Cette itération couvre les 4 evals, y compris le handoff vers `c4-modeling-process`, et remplace le faux baseline précédent par un vrai `without_skill`.
- Le skill discrimine surtout sur la rigueur de recadrage multi-projet : `list-projects`, `read-project-summary`, specs partagées et taxonomie valide avant édition.
- Chrono et tokens indisponibles : timing.json et benchmark forcés à 0. Ordre des configurations et delta normalisés.
