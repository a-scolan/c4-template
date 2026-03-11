# Skill Benchmark: troubleshoot-errors

**Model**: GPT-5.4
**Date**: 2026-03-10T18:20:00Z
**Evals**: 0, 1 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 33% ± 0% | +0.67 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- Le skill apporte surtout la lecture par cause racine : kinds valides, FQN complets, puis correction ciblée.
- Sur la dynamic view, le baseline sait parfois proposer un correctif local, mais n’explique pas les contraintes conceptuelles qui provoquent l’erreur.
- Les attentes discriminent bien la différence entre réparer à l’aveugle et expliquer pourquoi la modélisation LikeC4 échoue.
- Temps et tokens sont à 0 dans cette itération faute de télémétrie exécuteur persistée.
