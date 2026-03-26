# Eval-0 — Lookup Element Kinds: API Kind and DB Relationships

## Prompt
I'm not sure whether my backend should use `Container_Api`, `Container_API`, or just `Container`, and which model relationships are valid toward a database. Give me the exact taxonomy and how to verify it in the active workspace.

## Response

The correct kind is **`Container_Api`** (CamelCase: capital A, lowercase p-i). `Container_API` does not exist in this workspace — that is a common typo. `Container` (plain) is a generic base and rarely used directly.

From `projects/shared/spec-containers.c4`:
```
Container_Api  #Container #Api  — standard API/service container
```

To verify: open `projects/shared/SPEC_CHEATSHEET.md` or read `spec-containers.c4` directly.

For **model relationships toward a `Container_Database`**, the valid kinds (from `spec-global.c4`) are:
- `-[reads]->` — reads data (query)
- `-[writes]->` — writes data (upsert, insert, delete)
- `-[calls]->` — generic synchronous call (when reads/writes don't fit)

Do **not** use `https`, `sql`, or `tcp` in the logical model — those are deployment-level relationship kinds only.

```likec4
api = Container_Api 'Upload API' {
	technology 'Node.js'
}
db = Container_Database 'Metadata DB' {
	technology 'PostgreSQL'
}
api -[reads]-> db 'Fetches metadata'
api -[writes]-> db 'Persists record'
```
# Eval-0 — Lookup Element Kind: External Customer Actor

## Prompt
What element kind should I use in LikeC4 to model an external customer who interacts with our web portal?

## Response

Use `Actor_Person` for an external customer.

This kind is defined in `projects/shared/spec-context.c4` and carries tags `#Actor #Person`. It renders as a person shape with blue color, representing external users of the system.

```likec4
customer = Actor_Person 'Customer'
```

For internal employees, use `Actor_Staff` (`#Actor #Staff`, green). For administrators, use `Actor_Admin` (`#Actor #Admin`, amber).

The `#Actor` family tag groups all C1-level human actors in `spec-context.c4`.
