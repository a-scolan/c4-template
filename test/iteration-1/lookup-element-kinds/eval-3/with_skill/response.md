Start from the repository’s declared taxonomy in `projects/shared/spec-containers.c4`. Do not guess from English labels.

Confirmed exact kinds:

- HTTP API → `Container_Api`
- Message queue → `Container_Queue`

For an async worker, do not assume a name such as `Container_Worker` or `Container_AsyncWorker`; those are not declared here. Check the actual declared kinds first. If no specific declared subtype fits, use the base `Container` rather than inventing a near match. If the role is specifically a processing service, `Container_ProcessingServer` is a real declared kind, but only use it when that label truly matches the design.

How to resolve similar-looking names in this repository:

1. Check `projects/shared/spec-containers.c4` as the source of truth for container kinds.
2. Compare the exact declared identifier, character for character.
3. Reject close spellings that are not declared, such as `Container_API`.
4. If MCP is available, `read-project-summary` can confirm the active taxonomy.

The rule is simple: exact repository declaration wins; guessing loses.
