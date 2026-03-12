Model Redis as an explicit **cache layer**, but keep Postgres visible as the **source of truth**.

In this workspace there is no dedicated cache-specific kind, so do **not** invent something like `Container_Cache`. Use an existing valid kind instead. A good fit here is `Container_DataServer` with Redis as the technology.

Example:

```likec4
model {
  catalog = System_Existing 'Catalog Service' {
    api = Container_Api 'Catalog API' {
      technology 'Node.js'
    }

    cache = Container_DataServer 'Redis Cache' {
      technology 'Redis'
      description 'Read cache for hot API queries; not the primary data store'
    }

    database = Container_Database 'Postgres' {
      technology 'PostgreSQL'
      description 'Canonical system of record'
    }
  }

  catalog.api -[reads]-> catalog.cache 'Read cached data' {
    technology 'Redis'
  }

  catalog.api -[reads]-> catalog.database 'Read on cache miss' {
    technology 'PostgreSQL'
  }

  catalog.api -[writes]-> catalog.database 'Persist canonical data' {
    technology 'PostgreSQL'
  }

  catalog.api -[writes]-> catalog.cache 'Refresh or invalidate cache entry' {
    technology 'Redis'
  }
}
```

That keeps the intent clear:

- Redis accelerates reads
- Postgres is still read on cache miss
- Postgres remains the primary, authoritative store
- Redis is supportive infrastructure, not a replacement database

The main modeling guardrail is: **never hide the database behind Redis as if the cache were the primary system of record.**