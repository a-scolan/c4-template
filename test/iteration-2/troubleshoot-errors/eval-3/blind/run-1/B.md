Root cause is model-layer duplication.

You modeled the same traffic twice:
- Logical element relationship in `model {}`: `webapp -[https]-> api`
- Repeated again between deployed instances in deployment

Why this becomes confusing:
- Logical relationships already capture system communication intent (including technology/protocol label).
- Re-encoding identical communication at deployment level duplicates semantics and can diverge.

Clean fix:
- Keep the canonical interaction once at the logical layer (element relationship).
- In deployment, model topology/placement/instances.
- Add deployment-level relationships only when runtime routing differs materially from logical design (e.g., proxy hop, mesh gateway, node-local sidecar path).

In short: one source of truth for intent, deployment only for runtime structure differences.