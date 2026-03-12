Do not guess the name. Start from the repository declarations in `projects/shared/spec-containers.c4` and only use kinds that appear there exactly.

Confirmed kinds from this repository:

- HTTP API: `Container_Api`
- Message queue: `Container_Queue`

For an async worker, there is no declared `Container_Worker` or `Container_AsyncWorker` in the shared container taxonomy. The closest valid repository kind used for background job processing is `Container_ProcessingServer`, and `projects/spec-showcase/containers.c4` uses it as a `Background job processor` connected asynchronously to `Container_Queue`.

When two names look similar, resolve it by exact declaration matching:

1. Check `projects/shared/spec-containers.c4` for the exact kind name.
2. If the spelling is not declared verbatim, treat it as invalid.
3. Confirm usage in repository examples such as `projects/template/system-model.c4` or `projects/spec-showcase/containers.c4`.

Example: `Container_Api` is declared, while `Container_API` is not.

If none of the declared specific kinds fits cleanly, use the generic `Container` rather than inventing a new kind.