# Skill Benchmark: create-sequence-view

**Model**: gpt-5.4
**Date**: 2026-03-10T17:53:04Z
**Evals**: 0, 1, 2 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 33% ± 0% | +0.67 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- Les trois baselines gardent une partie de la forme LikeC4, mais ratent systématiquement au moins une règle centrale : mauvais type de vue, kind relationnel interdit, acteur initiateur manquant ou restriction parent→child ignorée.
- L'eval parent-child est la plus discriminante : sans le skill, la proposition conserve le lien invalide `api_container -> api_container.auth_component`, alors que la version avec skill le réécrit correctement vers l'acteur -> composant.
- Le skill ne gagne pas seulement sur la syntaxe ; il gagne aussi sur la causalité narrative, avec des labels d'action et un ordre temporel explicite sur le flux asynchrone.
- La télémétrie temps/tokens n'était pas disponible pour ces runs inline ; les métriques de temps et de tokens restent donc des placeholders à 0.