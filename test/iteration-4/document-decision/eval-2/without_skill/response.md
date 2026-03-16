Yes. This is clearly ADR-worthy because it changes a real architectural boundary and an external dependency strategy.
Suggested ADR frame:
- Title: Replace internal payment orchestration with direct Stripe integration behind a thin internal adapter
- Status: Proposed
- Context: The internal orchestration service adds maintenance cost, slows change delivery, and duplicates capabilities already available in Stripe. The system still needs a stable internal boundary so domain code is not tightly coupled to vendor APIs.
- Decision: Use Stripe as the primary payment platform, retire the broad internal orchestration service, and keep a small internal adapter responsible for request mapping, webhook/event normalization, idempotency, error translation, and configuration.
- Key drivers: Reduced system complexity, faster delivery, lower operational burden, clearer ownership, and access to mature SaaS payment features.
- Alternatives considered: Keep the internal orchestration service; build a broader provider-agnostic abstraction.
- Consequences: Less infrastructure to own and faster feature work, but stronger vendor dependence, Stripe-specific knowledge, migration effort, and the need to manage API/version/webhook changes carefully.
- Notes to include: lock-in rationale, PCI/compliance boundaries, observability, retries/failure handling, migration/cutover plan, and what must remain abstracted versus what can be Stripe-specific.
