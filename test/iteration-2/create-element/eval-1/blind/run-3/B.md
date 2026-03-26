# `Container_UploadOrchestrator` — Wrong Approach

Creating this kind for one service violates the core **shared-spec-first rule**.

## Why

The skill identifies this exact pattern as a bad decision:
> "Invent `Container_UploadOrchestrator` for a single service when `Container_Api` or another declared kind already fits"

Kind names describe **structural shape** (API, queue, database…), not business responsibility. Business responsibility goes in the element's **name and description**.

## Steps Before Adding a New Kind

1. **`projects/shared/SPEC_CHEATSHEET.md`** — scan all declared kinds.
2. **`projects/shared/spec-containers.c4`** — confirm exact names and intent.
3. Ask: does `Container_Api` cover the structural shape of this service?
4. If yes → use `Container_Api`; express specifics in name/description.
5. If no existing kind fits → propose adding it to **shared specs**, not as a local one-off.

## Correct Approach

```likec4
uploadOrchestrator = Container_Api 'Upload Orchestrator' {
  technology 'Node.js, Fastify'
  description 'Coordinates file validation, storage, and downstream event emission during upload.'
}
```

`Container_Api` fits an orchestrator that exposes an HTTP interface. The name and description carry the domain specifics.
