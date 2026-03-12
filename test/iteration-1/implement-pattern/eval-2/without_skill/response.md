Model Redis as an explicit cache in front of Postgres, but keep Postgres as the source of truth.

```likec4
cache = Container 'Redis Cache' {
  technology 'Redis'
  description 'Explicit cache layer for hot data'
}

vault.api -[reads]-> cache 'Reads cached data'
vault.api -[writes]-> cache 'Updates cached entry'

vault.api -[reads]-> postgres 'Reads on cache miss'
vault.api -[writes]-> postgres 'Persists authoritative data'
```

The important part is the behavior you describe around those links:

- `vault.api` reads from Redis first.
- On a cache miss, `vault.api` reads from Postgres.
- Writes still go to Postgres as the authoritative store.
- Redis is only an acceleration layer, not the primary datastore.

Do not model Redis as if it replaces Postgres or becomes the only read/write destination.