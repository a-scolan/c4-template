Model it as two explicit read relationships, not one "smart" relationship.

```likec4
vault.api -[reads]-> vault.redis 'Check cache'
vault.api -[reads]-> vault.postgres 'Load on cache miss'
```

Do not invent a composite kind such as `reads_with_fallback`. Keep the fallback intent in the labels if it helps, and keep detailed timing or branching behavior out of the relationship type. If that detail matters, capture it in a sequence view.
