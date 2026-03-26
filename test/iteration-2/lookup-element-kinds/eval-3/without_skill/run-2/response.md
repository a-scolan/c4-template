# Eval-3 — Lookup Element Kinds: API, Worker, Queue (run-2)

## Prompt
I'm looking for exact kinds for an HTTP API, an async worker, and a message queue, but I don't want to guess. How do you find them in the active workspace, and how do you resolve it when two names look similar?

## Response

**How to find exact kinds:**
1. Read `projects/shared/SPEC_CHEATSHEET.md` for the quick overview
2. Read `projects/shared/spec-containers.c4` for the full container kind definitions with tags and descriptions

**Exact kinds in this workspace:**
- **HTTP API** → `Container_Api` — tags `#Container #Api`
- **Async worker / processing service** → `Container_ProcessingServer` — tags `#Container #ProcessingServer` (or check spec for the exact name)
- **Message queue** → `Container_Queue` — tags `#Container #Queue`, queue shape

**When two names look similar**, compare their tags:
- `Container_Api` has `#Api` tag (for HTTP endpoints)
- `Container_ProcessingServer` has `#ProcessingServer` tag (for processing/worker services)

If you're unsure between two similar kind names, search `spec-containers.c4` for the exact PascalCase name and its `#` tags.

```likec4
api = Container_Api 'API Gateway' {
  technology 'Node.js'
}
queue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
}
worker = Container_ProcessingServer 'File Processor' {
  technology 'Go'
}
```
# Eval-3 — Lookup Element Kind: Database

## Prompt
I want to model a PostgreSQL relational database in my LikeC4 architecture. What element kind should I use?

## Response

Use `Container_Database` for a relational database.

From `projects/shared/spec-containers.c4`: tags `#Container #Database`, color `storage` (`#f59e0b`), shape `storage`, with a database icon.

```likec4
db = Container_Database 'Metadata DB' {
  technology 'PostgreSQL'
}
```

Related storage kinds:
- `Container_DatabaseGeo` — geographic/spatial databases
- `Container_ObjectStorage` — blob/object stores
- `Container_DataServer` — general data servers
- `Container_FileServer` — file system servers
- `Container_Directory` — LDAP/directory services

`Container_Database` is the correct choice for any relational or NoSQL database at the C2 container level.
