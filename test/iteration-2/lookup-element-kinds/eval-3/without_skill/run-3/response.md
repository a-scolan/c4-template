# Eval-3 — Lookup Element Kinds: API, Worker, Queue (run-3)

## Prompt
I'm looking for exact kinds for an HTTP API, an async worker, and a message queue, but I don't want to guess. How do you find them in the active workspace, and how do you resolve it when two names look similar?

## Response

**Finding exact kinds — always read the spec:**
- Open `projects/shared/spec-containers.c4`
- Look for declarations like `Container_Api is "Container" { ... }` with their `#` tags

**Confirmed kinds in this workspace:**

| Role | Kind | Tags |
|------|------|------|
| HTTP API | `Container_Api` | `#Container #Api` |
| Async worker | `Container_ProcessingServer` | `#Container #ProcessingServer` |
| Message queue | `Container_Queue` | `#Container #Queue` |

**Resolving similar-looking names:**
When two names look similar (e.g., `Container_Api` vs `Container_ApiGateway`), check:
1. Their `#` tags — distinct tags mean distinct roles
2. The `description` field in `spec-containers.c4`
3. Example usage in `projects/spec-showcase/` (for visual reference only, NOT authoritative)

Always use the kind whose description matches your intent, not just the closest-sounding name.

```likec4
api = Container_Api 'REST API' { technology 'Go' }
queue = Container_Queue 'Job Queue' { technology 'RabbitMQ' }
worker = Container_ProcessingServer 'Async Worker' { technology 'Python' }
```
# Eval-3 — Lookup Element Kind: Database

## Prompt
I want to model a PostgreSQL relational database in my LikeC4 architecture. What element kind should I use?

## Response

Use `Container_Database` for a relational database.

In `projects/shared/spec-containers.c4`, `Container_Database` has tags `#Container #Database`. It applies the `storage` color (orange-amber `#f59e0b`) and a `storage` shape to visually distinguish data stores from services.

```likec4
db = Container_Database 'Metadata DB' {
  technology 'PostgreSQL'
}
```

Storage-family alternatives:
- `Container_DatabaseGeo` — adds geo-specific iconography
- `Container_ObjectStorage` — blob or object storage (S3-style)
- `Container_DataServer` — data server / data source
- `Container_FileServer` — network file server

For PostgreSQL, `Container_Database` is the correct and standard kind.
