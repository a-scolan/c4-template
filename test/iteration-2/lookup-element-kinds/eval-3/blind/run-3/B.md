Exact kind guidance without guessing:

- HTTP API → `Container_Api`
- Message queue → `Container_Queue`

For an async worker, pick from declared kinds only (often `Container_ProcessingServer` if appropriate), never from invented labels.

Resolution method for similar names:

1. Read declared kinds from the active workspace specs.
2. Prefer exact identifier match.
3. Reject lookalikes (`Container_API`, `Node_VM`, `Infra_Firewall`, etc.).