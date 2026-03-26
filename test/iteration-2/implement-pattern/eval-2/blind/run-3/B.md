# Eval-2 — Implement Caching Layer Pattern (Baseline, Run 3)

## Prompt

> Implement a cache-aside pattern. Add a caching service (e.g. Redis) between the API layer and the primary database. Model the read-path (check cache first, fall back to DB) and write-path (write to DB and invalidate cache) using appropriate element kinds and relationship types from the shared spec.

---

## Response

Implementing cache-aside: the application first checks Redis, and only queries PostgreSQL when the cache misses. Successful reads are then populated into the cache.

### Model additions

```likec4
model {
  system DataPlatform 'Data Platform' {
    service = Container_Api 'Data Service' {
      technology 'FastAPI'
    }

    redisNode = Container 'Redis' {
      technology 'Redis 7'
      description 'Cache node for query results'
    }

    postgres = Container_Database 'PostgreSQL' {
      technology 'PostgreSQL 16'
    }

    service -> redisNode 'Cache lookup' { technology 'Redis' }
    service -> postgres 'DB query (miss)' { technology 'SQL' }
    service -> redisNode 'Cache set' { technology 'Redis' }
    service -> postgres 'Write' { technology 'SQL' }
  }
}
```

### View

```likec4
views {
  view data_tier of DataPlatform {
    title 'Cache-Aside — Data Tier'
    include *
    autoLayout TopBottom
  }
}
```

---

## Observations (baseline, no skill)

- Cache not tagged with `#Data` or `#Persistence`
- Should use `-[reads]->` and `-[writes]->` relationship kinds from the shared spec
- Cache operations not differentiated by direction in visual representation
- No tag-based filtering in views to isolate cache paths
