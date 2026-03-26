# Eval-1 — Lookup Element Kinds: Deployment Relationship Kinds (run-3)

## Prompt
Between an app VM and a database VM in deployment, should I use `calls`, `tcp`, or `sql`? And in the logical application model, what remains valid?

## Response

**`calls` is a logical model kind only** — never use it in deployment.

**Deployment (between VMs or instances):**
- `sql` — for SQL database connections (defined in `spec-deployment.c4` / `spec-global.c4`)
- `tcp` — generic TCP transport for other scenarios

**Logical model (`model {}`):**
- `reads` — data reads from the database
- `writes` — data writes to the database
- `calls` — generic synchronous call (valid in the logical model, not deployment)

The relationship kind lives in the logical model to describe business intent. The deployment section describes physical transport (sql, tcp, https, amqp...).

Tags: `reads` and `writes` edges inherit no special tags; they are plain relationship kinds.

```likec4
// Logical: business relationship
uploadService -[writes]-> documentDb 'Persist file metadata'
retrievalService -[reads]-> documentDb 'Query file metadata'

// Deployment: physical connection
Prod.AppTier.UploadVm -[sql]-> Prod.DataTier.DbVm 'MongoDB wire protocol'
```
# Eval-1 — Lookup Element Kind: Internal Staff User

## Prompt
I need to model an internal employee (staff member) who uses our back-office admin tool. What element kind should I use?

## Response

Use `Actor_Staff` for an internal employee.

From `projects/shared/spec-context.c4`: `Actor_Staff` has tags `#Actor #Staff` and uses a green person shape. It is designated for internal users of the organization.

```likec4
backOfficeUser = Actor_Staff 'Back-Office User'
```

Distinction from siblings:
- `Actor_Person` (`#Actor #Person`) — external parties, blue
- `Actor_Admin` (`#Actor #Admin`) — administrators, amber

For a regular internal staff member with no elevated admin rights, `Actor_Staff` is the correct kind.
