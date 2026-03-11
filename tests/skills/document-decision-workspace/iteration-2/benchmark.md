# Skill Benchmark: document-decision

**Model**: GPT-5.4
**Date**: 2026-03-10T17:53:33Z
**Evals**: 0, 1 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 29% ± 6% | +0.71 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- L'eval CI/CD discrimine bien le périmètre : le skill refuse correctement un ADR hors architecture système.
- Le baseline garde parfois l'idée de tracer la décision, mais sans cadre ADR ni trade-offs structurés.
- Les métriques temps/tokens valent 0 ici faute de métadonnées d'exécution récupérables dans cette session ; compare surtout les pass rates.
- Cette itération n'a qu'1 run par configuration : la tendance est utile, mais encore peu robuste statistiquement.