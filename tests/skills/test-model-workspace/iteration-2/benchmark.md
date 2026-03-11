# Skill Benchmark: test-model

**Model**: GPT-5.4
**Date**: 2026-03-10T18:10:00Z
**Evals**: 0, 1 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 33% ± 0% | +0.67 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- Le skill impose une séquence de validation complète (structure -> références -> relations -> rendu -> Problems) que le baseline ne reconstruit pas spontanément.
- L’eval de contexte de vue discrimine bien la valeur du skill : le baseline parle d’includes et de rendu, mais oublie le contexte parent et le handoff vers `design-view`.
- Les métriques temps/tokens restent à 0 dans cette itération car aucun exécuteur séparé n’a exposé de télémétrie récupérable.
- Une seule exécution par configuration suffit pour une comparaison directionnelle, mais pas pour mesurer la variance.
