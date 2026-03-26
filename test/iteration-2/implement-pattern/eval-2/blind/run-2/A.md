Pattern: **Cache in front of source-of-truth database**.

Model Redis as read acceleration and Postgres as authoritative store.

```likec4
cache = Container 'Redis Cache' {
  technology 'Redis'
  description 'Fast lookup layer.'
}

database = Container_Database 'Postgres' {
  technology 'PostgreSQL'
  description 'Canonical persistent storage.'
}

api -[reads]-> cache 'Attempts cache read first'
api -[reads]-> database 'Falls back on miss'
api -[writes]-> database 'Commits authoritative update'
api -[writes]-> cache 'Refreshes or invalidates cached data'
```

Key modeling intent:
- Keep writes authoritative on Postgres, so Redis is clearly additive caching rather than replacement storage.

Substitutions:
- Replace kinds/relationship names with your declared workspace spec.
- Swap placeholder names and technology labels as needed.