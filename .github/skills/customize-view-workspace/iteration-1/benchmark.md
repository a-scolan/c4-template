# Skill Benchmark: customize-view

**Model**: gpt-5.4
**Date**: 2026-03-10T17:53:05Z
**Evals**: 0, 1, 2 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 11% ± 19% | +0.89 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- Les baselines dérivent immédiatement vers des hex colors locaux ou des cibles `navigateTo` instables, alors que le skill maintient systématiquement palette partagée et IDs de vues existants.
- L'eval palette partagée montre une baseline partiellement utile (présence de règles `style`) mais encore insuffisante : elle échoue sur la gouvernance de palette et sur la préservation explicite du contexte.
- Le score très faible de la baseline vient surtout de deux écarts récurrents : personnalisation hors périmètre (ajouts structurels) et absence de lien/navigation stables.
- La télémétrie temps/tokens n'était pas disponible pour ces runs inline ; les métriques de temps et de tokens restent donc des placeholders à 0.