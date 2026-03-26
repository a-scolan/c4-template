# Eval-2 — Implement Caching Layer Pattern (Baseline, Run 1)

## Prompt

> Implement a cache-aside pattern. Add a caching service (e.g. Redis) between the API layer and the primary database. Model the read-path (check cache first, fall back to DB) and write-path (write to DB and invalidate cache) using appropriate element kinds and relationship types from the shared spec.

---

## Response

I will introduce a Redis cache between the API and the database. The API checks the cache first; on a miss it reads from the database and populates the cache.

### Model additions

```likec4
model {
  system CachingDemo 'Caching Demo' {
    api = Container_Api 'API Service' {
      technology 'Node.js'
      description 'Serves data to clients with cache-aside logic'
    }

    cache = Container 'Redis Cache' {
      technology 'Redis'
      description 'In-memory cache for frequent reads'
    }

    database = Container_Database 'Primary Database' {
      technology 'PostgreSQL'
      description 'Source of truth for persistent data'
    }

    api -> cache 'Reads cached data' { technology 'Redis' }
    api -> database 'Falls back on cache miss' { technology 'SQL' }
    api -> database 'Writes data' { technology 'SQL' }
    api -> cache 'Invalidates on write' { technology 'Redis' }
  }
}
```

### View

```likec4
views {
  view cache_pattern of CachingDemo {
    title 'Cache-Aside Pattern'
    include *
    autoLayout TopBottom
  }
}
```

---

## Observations (baseline, no skill)

- Redis modeled as generic `Container` — should use a typed kind or `#Data` tag
- Relationships use `->` without typed kinds (`reads`, `writes`, `async`)
- Read and write caching paths not visually distinguished
- No `#Persistence` or `#Data` tags appliedModel Redis as a cache layer, while keeping Postgres as source of truth.

- `Container_Database 'Redis Cache'` with `technology 'Redis'`
- `Container_Database 'Postgres'` with `technology 'PostgreSQL'`
- API reads cache first, falls back to Postgres on miss
- API writes remain explicit to Postgres; cache is updated/refreshed separately

Recommended pattern:

```likec4
api = Container_Api 'Catalog API'
redis = Container_Database 'Redis Cache' {
  technology 'Redis'
}
postgres = Container_Database 'Postgres' {
  technology 'PostgreSQL'
}

api -[reads]-> redis 'Lookup cached data' {
  technology 'Redis'
}

api -[reads]-> postgres 'Cache miss fallback' {
  technology 'PostgreSQL'
}

api -[writes]-> postgres 'Persist source of truth' {
  technology 'PostgreSQL'
}

api -[writes]-> redis 'Refresh/invalidate cache entries' {
  technology 'Redis'
}
```

Mistake to avoid: only showing Redis reads/writes and omitting explicit Postgres persistence/read-fallback, which suggests Redis replaced the database.