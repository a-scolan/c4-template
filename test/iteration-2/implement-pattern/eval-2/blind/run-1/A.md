Pattern: **Cache + source of truth**.

Model Redis as a cache in front of Postgres, while keeping Postgres as canonical persistence.

```likec4
cache = Container 'Redis Cache' {
  technology 'Redis'
  description 'Hot-data cache for read acceleration.'
}

database = Container_Database 'Postgres' {
  technology 'PostgreSQL'
  description 'Source-of-truth data store.'
}

api -[reads]-> cache 'Checks cache first'
api -[reads]-> database 'Reads on cache miss'
api -[writes]-> database 'Persists authoritative changes'
api -[writes]-> cache 'Refreshes/invalidate cached values'
```

Why this avoids the wrong implication:
- The write path always includes Postgres, so Redis is explicitly an optimization layer, not a replacement.

Substitutions:
- `exact kinds`: replace generic `Container`/`Container_Database` and `reads`/`writes` with your declared types.
- `names`: align with your existing API/cache/database identifiers.
- `tech`: keep Redis/Postgres only if that is your actual stack.