Model it as **two explicit read relationships**, not one “smart” relationship.

```likec4
api -[reads]-> redis 'Checks cache'
api -[reads]-> postgres 'Fetches on cache miss'
```

Do **not** invent a composite kind such as `reads_with_fallback`. Keep the relationship kinds simple and explicit:
- `-[reads]->` for Redis
- `-[reads]->` for PostgreSQL

If you want to document the fallback behavior, put that in the action labels (for example, `'Checks cache'` and `'Fetches on cache miss'`) or show the timing in a dynamic/sequence view. The fallback logic should not live in the relationship type itself.
