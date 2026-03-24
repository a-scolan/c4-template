Pattern: Cache plus source of truth.

Minimal scaffold:
cache = Container 'Redis Cache' {
  technology 'Redis'
  description 'Hot-data cache.'
}

api -[reads]-> cache 'Checks cache'
api -[reads]-> database 'Fetches on cache miss'
api -[writes]-> cache 'Refreshes cache'
api -[writes]-> database 'Persists source-of-truth changes'

How to keep the model accurate:
- Keep Postgres as the source of truth.
- Show both cache access and database access so the diagram does not imply Redis replaces the database.
- If your workspace provides a more specific cache/container kind, use that instead of the generic `Container`.

Substitute before finalizing:
- parent: place `cache` under the same service boundary as the API
- exact kinds: use the declared cache/database kinds and `reads`/`writes` relationship names from your workspace
- names: replace `cache` and `database` with your real Redis/Postgres element names
- tech: `Redis` for the cache and `PostgreSQL` for the database
