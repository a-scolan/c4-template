# Skill Benchmark: test-model

**Model**: GPT-5.4
**Date**: 2026-03-10T17:31:01Z
**Evals**: 0, 1 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 33% ± 0% | +0.67 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0.0 ± 0.0 | 0.0 ± 0.0 | +0 |

## Notes

- L'eval de handoff vers `design-view` discrimine bien le skill : le baseline parle rendu/includes mais ne renvoie pas le skill spécialisé.
- Le skill ajoute une vraie séquence de validation (structure → références → relations → rendu), alors que le baseline reste partiel.
- Les métriques temps/tokens valent 0 ici faute de métadonnées d'exécution récupérables dans cette session ; compare surtout les pass rates.
- Cette itération n'a qu'1 run par configuration : la tendance est utile, mais encore peu robuste statistiquement.
