# Skill Benchmark: structure-deployment-tiers

**Model**: GPT-5.4  
**Date**: 2026-03-10T18:15:00Z  
**Evals**: 0, 1 (1 run per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 17% ± 24% | +0.83 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- Évaluation manuelle : temps et tokens indisponibles, valeurs fixées à 0.
- L'eval de topologie discrimine bien la séparation des tiers : le baseline mélange le traitement async avec l'applicatif.
- L'eval de handoff confirme le périmètre : le skill reste centré sur les tiers et renvoie le détail d'infrastructure à `model-deployment-infrastructure`.
- Cette itération n'a qu'1 run par configuration ; la tendance est utile, mais reste peu robuste statistiquement.
