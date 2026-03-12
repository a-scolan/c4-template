The safe way is to start from the repository’s declared taxonomy, not from memory and definitely not from vibes.

How to find them in the active workspace:

1. Open the active project's `likec4.config.json` and confirm it includes `../shared`.
2. Read `projects/shared/spec-containers.c4` for the declared container kinds.
3. If available, compare that against `read-project-summary` so you are looking at the active project’s resolved taxonomy.

Confirmed exact kinds from this workspace:

- HTTP API: `Container_Api`
- Message queue: `Container_Queue`

For an async worker, do **not** guess a name like `Container_Worker` unless it is actually declared. In the shared container spec, there is no dedicated `Container_Worker` kind. The closest confirmed declared kind for a background processing service is `Container_ProcessingServer`; if that does not fit, fall back to the generic `Container` rather than inventing a new subtype.

How to resolve similar names:

- Compare the exact declared identifier in the spec.
- Prefer the repository spelling over the more readable English-looking variant.
- Example: use `Container_Api`, reject `Container_API`.

So the pattern is: confirm the exact declared name, reject lookalikes, and if a specialized worker kind is not declared, use the nearest real kind (`Container_ProcessingServer`) or the generic `Container` until you define something explicit.