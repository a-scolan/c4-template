For this workspace, exact known kinds include:

- HTTP API: `Container_Api`
- Message queue: `Container_Queue`

For an async worker, do not guess a non-declared `Container_Worker`. Resolve from declared kinds, typically using a valid container subtype such as `Container_ProcessingServer` (or another declared container kind matching your implementation).

How to find exact kinds safely:

1. Inspect declared element kinds in the active project/spec files.
2. Confirm exact spelling in `projects/shared/spec-containers.c4`.
3. If two names look similar, keep only the exact declared identifier and reject lookalikes.

Example of lookalike resolution:

- Keep `Container_Api`
- Reject `Container_API`

Same principle applies to deployment (`Infra_Fw` vs `Infra_Firewall`, `Node_Vm` vs `Node_VM`).