# Skill Benchmark: implement-pattern

**Model**: GPT-5.4
**Date**: 2026-03-10T18:40:00Z
**Evals**: 0, 1, 2 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 22% ± 19% | +0.78 |
| Time | 0.0s ± 0.0s | 0.0s ± 0.0s | +0.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- Le skill transforme des conseils génériques en patrons LikeC4 concrets : kinds dédiés, relations typed et garde-fous de modélisation.
- L’intégration externe discrimine très fortement le skill : sans lui, la réponse n’invente pas naturellement `System_External`, `#External` et `-[calls]->` ensemble.
- Le baseline retrouve parfois l’idée métier (queue RabbitMQ, cache Redis), mais pas la notation typed ni les responsabilités explicites du pattern.
- La variance non nulle du baseline vient du fait que certains prompts suggèrent naturellement le composant (queue/cache) sans pour autant amener la bonne modélisation LikeC4.
