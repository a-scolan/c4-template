Model this as a **caching layer** in front of Postgres, not as a database replacement.

Add an explicit Redis cache, for example:

`cache = Container_Cache 'Cache' { technology 'Redis'; description 'Low-latency cache for hot reads' }`

Then use typed data-access relationships from `vault.api`:

- `vault.api -[reads]-> cache 'Read-through cache'`
- `vault.api -[writes]-> cache 'Cache updates'`
- `vault.api -[reads]-> vault.database 'Fetch on cache miss'`

This keeps the meaning clear:

- Redis accelerates hot reads.
- Postgres remains the **source of truth**.
- The cache is not the primary store; it only supports faster access.