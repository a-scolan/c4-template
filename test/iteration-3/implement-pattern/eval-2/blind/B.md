Use the Cache + source-of-truth pattern.

Minimal scaffold:
redisCache = Container 'Redis Cache' {
  technology 'Redis'
}

postgresDb = Container_Database 'Postgres' {
  technology 'PostgreSQL'
}

api -[reads]-> redisCache 'Checks cache' {
  technology 'Redis'
}

api -[reads]-> postgresDb 'Loads on cache miss' {
  technology 'PostgreSQL'
}

api -[writes]-> redisCache 'Refreshes cached data' {
  technology 'Redis'
}

api -[writes]-> postgresDb 'Persists canonical change' {
  technology 'PostgreSQL'
}

Why this stays safe:
- This workspace does not define a cache-specific element kind, so use a valid generic `Container` for Redis rather than inventing something like `Container_Cache`.
- Use `reads` and `writes` for both cache and database access.
- Keep the database as the source of truth: the cache is an optimization layer, not the primary store.
- The database read on cache miss is important because it shows Redis accelerates reads without replacing Postgres.

Substitute:
- your real API name
- exact cache refresh/invalidation labels
- parent system/container names to fit your model
