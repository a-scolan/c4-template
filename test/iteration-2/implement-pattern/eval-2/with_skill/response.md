Model it as a **read-through cache** in front of the database, while keeping Postgres as the source of truth.

In this workspace, the shared spec defines `Container_Database` but does **not** define a dedicated cache-specific container kind in the cheat sheet, so use a valid declared kind such as the generic `Container` and make the cache role explicit in the title and technology.

```likec4
api = Container_Api 'Read API' {
  technology 'Node.js'
}

cache = Container 'Redis Cache' {
  technology 'Redis'
  description 'Low-latency cache for hot reads'
}

database = Container_Database 'Postgres' {
  technology 'PostgreSQL'
}

api -[reads]-> cache 'Read-through cache lookup'
api -[writes]-> cache 'Cache updates / invalidation'
api -[reads]-> database 'Fetch on cache miss' {
  technology 'PostgreSQL'
}
api -[writes]-> database 'Persist source-of-truth changes' {
  technology 'PostgreSQL'
}
```

Key point: the cache accelerates hot reads, but the database remains the **authoritative source of truth**. Do not model Redis as replacing Postgres or as the primary store.
