Model it as **two explicit `reads` relationships**, not one “smart” relationship.

Why: each edge should represent a concrete dependency.

Example:

- `api -[reads]-> redis "Cache lookup" { technology "REDIS" }`
- `api -[reads]-> postgres "Fallback on cache miss" { technology "PostgreSQL" }`

If you want to show the conditional behavior (cache hit/miss), use a dynamic/sequence-style view in addition to these structural edges.
