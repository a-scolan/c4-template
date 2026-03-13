Yes, this is a strong ADR candidate. A sensible file path would be `ADR/0002-stripe-direct-payment-integration.md`.

## Status
Proposed

## Context
The current payment flow goes through an internal payment orchestration service. That service adds ownership and operational overhead, while much of the required capability is already available from Stripe. The proposed direction is to integrate directly with Stripe and retain only a small internal adapter boundary so the rest of the system does not depend directly on Stripe APIs, payloads, and webhook formats.

## Decision
Retire the internal payment orchestration service as the primary integration path. Use Stripe as the external provider boundary, and keep a thin internal adapter, for example `Payments.paymentAdapter`, as the only internal layer that communicates with Stripe. This affects the internal service being removed, the retained adapter boundary, the calling application or service, and any views or operational documentation that show payment flows or webhook ingress. Out of scope: unrelated order or billing domain redesign.

## Impacted Elements
- Internal orchestration service to be decommissioned, for example `Payments.paymentOrchestrationService`
- Retained adapter boundary, for example `Payments.paymentAdapter`
- Calling service or API, for example `Commerce.checkoutApi`
- External provider boundary: `Stripe`
- Any context/container/deployment views that show payment processing, webhook ingress, retries, secrets, or operational ownership

## Consequences
### Positive
- Reduces internal platform surface area and maintenance burden
- Accelerates access to Stripe features and provider-managed capabilities
- Keeps a controlled adapter seam so the rest of the system is insulated from raw Stripe payloads and API changes

### Negative
- Increases dependency on a third-party SaaS provider and its API/versioning model
- Reduces control compared with a fully internal orchestration layer
- Requires careful webhook handling, idempotency design, secret management, and failure recovery
- Makes future provider substitution harder unless the adapter contract stays disciplined

## Follow-up
- Define the migration scope from the old orchestration service to the adapter-plus-Stripe path
- Model webhook ingress, retries, reconciliation, and idempotency responsibilities
- Update validation and error-mapping behavior in the internal adapter
- Clarify operational ownership for Stripe credentials, monitoring, and incident response
- Update affected views and supporting operations documentation
