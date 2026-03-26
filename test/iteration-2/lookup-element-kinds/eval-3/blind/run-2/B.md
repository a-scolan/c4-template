Exact kind lookup in this workspace:

- HTTP API: `Container_Api`
- Message queue: `Container_Queue`

For an async worker, do not invent a kind. Choose from declared container kinds (commonly `Container_ProcessingServer` when it fits), after verification.

How to find and resolve similar names:

1. Inspect declared kinds in the active workspace specs.
2. Confirm exact names in `projects/shared/spec-containers.c4`.
3. If two options look similar, keep the exact declared one and reject the lookalike.

Example:

- Keep `Container_Api`
- Reject `Container_API`