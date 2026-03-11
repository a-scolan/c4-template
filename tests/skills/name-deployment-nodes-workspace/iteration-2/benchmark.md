# Skill Benchmark: name-deployment-nodes

**Model**: GPT-5.4  
**Date**: 2026-03-10T18:10:00Z  
**Evals**: 0, 1 (1 run per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 17% ± 24% | +0.83 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- Évaluation manuelle : temps et tokens indisponibles, valeurs fixées à 0.
- L'eval de correction de noms discrimine fortement : le baseline conserve `VM`, le snake_case et des zones trop génériques.
- L'eval de handoff vérifie bien le périmètre : le skill recentre sur le naming et renvoie la modélisation détaillée à `model-deployment-infrastructure`.
- Cette itération n'a qu'1 run par configuration ; la tendance est utile, mais reste peu robuste statistiquement.
