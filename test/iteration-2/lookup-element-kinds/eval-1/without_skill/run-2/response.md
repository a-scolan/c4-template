# Eval-1 — Lookup Element Kinds: Deployment Relationship Kinds (run-2)

## Prompt
Between an app VM and a database VM in deployment, should I use `calls`, `tcp`, or `sql`? And in the logical application model, what remains valid?

## Response

**In the deployment model** (between `Node_Vm` instances or `Node_App` instances):
- Use **`sql`** when the connection is specifically SQL-based (PostgreSQL, MySQL)
- Use **`tcp`** for generic TCP transport (when no specific protocol kind fits)
- `calls` is a **logical model** relationship kind — do not use it in deployment

These deployment relationship kinds are defined in `projects/shared/spec-deployment.c4` (or `spec-global.c4`).

**In the logical application model** (`model {}`):
- `-[reads]->` — when the service reads data from the database
- `-[writes]->` — when the service writes data to the database
- `-[calls]->` — generic synchronous call (fallback when reads/writes don't fit)

`sql`, `tcp`, `https` are NOT valid in the logical model block.

```likec4
// Logical model (system-model.c4)
api -[reads]-> db 'Fetch metadata'
api -[writes]-> db 'Persist record'

// Deployment model (deployment.c4)
Prod.AppTier.ApiVm -[sql]-> Prod.DataTier.DbVm 'Query database'
```
# Eval-1 — Lookup Element Kind: Internal Staff User

## Prompt
I need to model an internal employee (staff member) who uses our back-office admin tool. What element kind should I use?

## Response

Use `Actor_Staff` for an internal employee.

Defined in `projects/shared/spec-context.c4`, this kind carries tags `#Actor #Staff` and renders as a person shape with green color, representing internal users of the system.

```likec4
backOfficeUser = Actor_Staff 'Back-Office User'
```

Within the `#Actor` family:
- `Actor_Person` — external customers (blue)
- `Actor_Staff` — internal employees (green)
- `Actor_Admin` — system administrators (amber)

`Actor_Staff` is the correct choice for internal non-admin staff at the C1 context level.
