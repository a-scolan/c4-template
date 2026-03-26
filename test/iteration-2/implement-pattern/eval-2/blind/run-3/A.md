Pattern: **Redis cache + Postgres source of truth**.

Model cache-as-optimization explicitly:

```likec4
redisCache = Container 'Redis Cache' {
  technology 'Redis'
  description 'Low-latency read cache.'
}

postgres = Container_Database 'Postgres' {
  technology 'PostgreSQL'
  description 'Authoritative system of record.'
}

api -[reads]-> redisCache 'Reads hot path first'
api -[reads]-> postgres 'Reads on cache miss'
api -[writes]-> postgres 'Writes authoritative data'
api -[writes]-> redisCache 'Updates/invalidates cache entries'
```

Why this is correct:
- Database remains authoritative for persistence; cache accelerates reads and mirrors selective state.

Substitutions:
- Map element/relationship kinds to your workspace taxonomy.
- Replace names with your canonical API/cache/database identifiers.
- Set technology labels to your real implementation details.