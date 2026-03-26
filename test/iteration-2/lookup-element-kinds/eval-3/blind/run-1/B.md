Exact kinds you can use in this workspace:

- HTTP API: `Container_Api`
- Message queue: `Container_Queue`
- Async worker: no dedicated `Container_Worker` kind is declared; use:
  - `Container` (generic), or
  - a declared specialized container that matches intent (for example `Container_ProcessingServer`)

How to find exact kinds (no guessing):
1. Open `projects/shared/spec-containers.c4`.
2. Read only names declared as `element <KindName>`.
3. Use those names exactly (case-sensitive).

How to resolve similar-looking names:
- Prefer names that are explicitly declared (e.g., `Container_Api`, not `Container_API`).
- If two declared names are both plausible, pick by semantic tags/notation in the declaration:
  - API behavior/tagging → `Container_Api`
  - messaging → `Container_Queue`
  - general compute service without dedicated kind → `Container` (or closest declared server subtype).