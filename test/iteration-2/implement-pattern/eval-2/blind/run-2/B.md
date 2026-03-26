# Eval-2 — Implement Caching Layer Pattern (Baseline, Run 2)

## Prompt

> Implement a cache-aside pattern. Add a caching service (e.g. Redis) between the API layer and the primary database. Model the read-path (check cache first, fall back to DB) and write-path (write to DB and invalidate cache) using appropriate element kinds and relationship types from the shared spec.

---

## Response

Adding a caching layer to improve read performance. The service will check the cache before querying the database.

### Model additions

```likec4
model {
  system App 'Application' {
    apiLayer = Container_Api 'API Layer' {
      technology 'Express'
      description 'REST API with cache-aside implementation'
    }

    redisCache = Container 'Cache' {
      technology 'Redis'
      description 'Key-value store for cached responses'
      style { shape storage }
    }

    mainDb = Container_Database 'Main DB' {
      technology 'MySQL'
      description 'Relational database for persistent storage'
    }

    // Cache read path
    apiLayer -> redisCache 'Checks cache' { technology 'Redis' }

    // Cache miss path
    apiLayer -> mainDb 'Reads on miss' { technology 'SQL' }

    // Write path
    apiLayer -> mainDb 'Writes data' { technology 'SQL' }
  }
}
```

### View

```likec4
views {
  view caching_view of App {
    title 'Caching Layer'
    include *
    autoLayout LeftRight
  }
}
```

---

## Observations (baseline, no skill)

- `Container` used for Redis (should have specific kind or `#Data` / `#Persistence` tag)
- `reads` and `writes` typed relationships not used (should be `-[reads]->` and `-[writes]->`)
- Cache invalidation on write not modeled
- No `#Cache` or storage color applied
