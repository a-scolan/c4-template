Do not guess; use the shared spec files as the source of truth.

Start here:
1. Read `projects/shared/spec-containers.c4` for the exact declared container kinds.
2. Use `projects/shared/SPEC_CHEATSHEET.md` as a quick cross-check.
3. Accept only names that appear exactly as declared in the spec.

Exact confirmed kinds from this workspace:
- HTTP API: `Container_Api`
- Message queue: `Container_Queue`

For an async worker, there is **no** declared exact kind named `Container_Worker` or `Container_AsyncWorker` in the shared taxonomy. If you need worker semantics, choose from the real declared kinds based on role; `Container_ProcessingServer` is the closest processing-oriented declared kind, but it should be verified from the spec rather than guessed.

When two names look similar, resolve them by exact spelling and casing against the declarations. Example: `Container_Api` exists, while `Container_API` does not. The same rule applies to every close-looking candidate.
