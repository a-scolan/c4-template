# Skill Benchmark: lookup-element-kinds

**Model**: GPT-5.4
**Date**: 2026-03-11T07:31:49Z
**Evals**: 0, 1, 2 (1 run each per configuration)

## Summary

| Metric | with_skill | without_skill | Delta |
|--------|---------------|----------------|-------|
| Pass Rate | 100% ± 0% | 92% ± 14% | +0.08 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 304 ± 63 | 220 ± 34 | +84 |

## Notes

- Configuration primaire : with_skill ; baseline : without_skill.
- Harness statique : timing.json et benchmark fixés à 0 pour le temps et les tokens.
- Ordre des configurations et signe du delta normalisés après agrégation.
- Correction factuelle appliquée : `Infra_Fw` remplace `Infra_Firewall` dans la réponse avec skill concernée.
