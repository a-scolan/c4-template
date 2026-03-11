# Skill Benchmark: design-view

**Model**: gpt-5.4
**Date**: 2026-03-10T17:53:03Z
**Evals**: 0, 1, 2 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 22% ± 19% | +0.78 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- L'eval C2 discrimine surtout sur la complétude structurelle : la baseline garde le bon dossier mais oublie parent explicite, voisinage relationnel et drill-down.
- L'eval Deployment sépare nettement les configurations : seule la version avec skill explicite correctement environnement, zones et VMs sans wildcard.
- L'eval de handoff montre que le skill apporte surtout une bonne répartition des responsabilités entre `design-view`, `create-sequence-view` et `customize-view`.
- La télémétrie temps/tokens n'était pas disponible pour ces runs inline ; les métriques de temps et de tokens restent donc des placeholders à 0.