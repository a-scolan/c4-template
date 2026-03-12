Use two explicit `reads` relationships:

```likec4
vault.api -[reads]-> redisCache 'Checks cache'
vault.api -[reads]-> postgresDb 'Reads on cache miss'
```

Do not invent a composite kind such as `reads_with_fallback` and do not try to collapse both dependencies into one “smart” relationship.

Keep fallback behavior outside the relationship type. If you want to document the intent, use clear labels like `Checks cache` and `Reads on cache miss`. If the exact fallback sequence matters, show that in a dynamic or sequence view instead of encoding it into the relationship kind.