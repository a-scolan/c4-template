# Skill Benchmark: troubleshoot-errors

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

- Les deux evals différencient bien diagnostic de cause racine vs corrections vagues ou symptomatiques.
- Le baseline repère parfois un symptôme, mais sans aller jusqu'au FQN complet ni aux contraintes conceptuelles de dynamic view.
- Les métriques temps/tokens valent 0 ici faute de métadonnées d'exécution récupérables dans cette session ; compare surtout les pass rates.
- Cette itération n'a qu'1 run par configuration : la tendance est utile, mais encore peu robuste statistiquement.
