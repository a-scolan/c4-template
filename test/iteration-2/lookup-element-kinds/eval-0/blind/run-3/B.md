# Eval-0 — Lookup Element Kinds: API Kind and DB Relationships (run-3)

## Prompt
I'm not sure whether my backend should use `Container_Api`, `Container_API`, or just `Container`, and which model relationships are valid toward a database. Give me the exact taxonomy and how to verify it in the active workspace.

## Response

Use **`Container_Api`** — this is the exact kind used in this workspace. `Container_API` (all-caps) does not exist. `Container` (plain) is a base kind and is rarely used directly in practice.

Check `projects/shared/spec-containers.c4` to verify. The SPEC_CHEATSHEET.md also lists all valid kinds.

Tags for `Container_Api`: `#Container #Api`

**Valid model relationship kinds toward a `Container_Database`:**
- `-[reads]->` — for data queries
- `-[writes]->` — for data mutations
- `-[calls]->` — generic synchronous invocation
- `-[async]->` — for asynchronous data delivery (less common toward a DB)

`sql`, `tcp`, `https` are deployment-layer relationship kinds (spec-global.c4 / spec-deployment.c4) and are NOT valid in the logical `model {}` block.

```likec4
service = Container_Api 'API Service' {
	technology 'Go'
}
db = Container_Database 'Document Store' {
	technology 'MongoDB'
}
service -[reads]-> db 'Query metadata'
service -[writes]-> db 'Persist document'
```
# Eval-0 — Lookup Element Kind: External Customer Actor

## Prompt
What element kind should I use in LikeC4 to model an external customer who interacts with our web portal?

## Response

Use `Actor_Person` for an external customer.

Defined in `projects/shared/spec-context.c4`, this kind carries tags `#Actor #Person`. It uses a person shape with blue styling and is intended for external users interacting with your system.

```likec4
customer = Actor_Person 'Customer'
```

Alternatives in the same family:
- `Actor_Staff` — internal employees (`#Actor #Staff`, green)
- `Actor_Admin` — administrators (`#Actor #Admin`, amber)

All actor kinds share the `#Actor` family tag, grouping human principals at the C1 context level.
