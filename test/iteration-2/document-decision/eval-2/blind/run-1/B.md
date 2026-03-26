# ADR Framing — Replace Internal Payment Orchestrator with Direct Stripe SaaS Integration

## Suggested filename
`ADR/0002-direct-stripe-integration-with-internal-adapter-boundary.md`

## Status
Proposed

## Context
We currently operate an internal payment orchestration service that adds maintenance and operational burden. We now want to integrate directly with Stripe while preserving a minimal internal adapter boundary to protect domain code from provider specifics.

Key forces:
- Need faster feature delivery for payment capabilities
- Desire to reduce platform ownership and operational load
- Need to preserve internal domain boundary and avoid Stripe lock-in leakage
- Security/compliance requirements (PCI scope, auditability, secrets handling)

## Decision
Adopt **direct SaaS integration to Stripe** for payment execution and lifecycle events, with a **small internal adapter boundary** that exposes stable internal interfaces.

In scope:
- Stripe API integration
- Provider webhook ingestion/verification
- Internal adapter abstraction for domain services

Out of scope:
- Building a new generic internal orchestration platform
- Multi-provider smart routing at this stage

## Impacted Elements
- Checkout/payment application services
- Existing internal payment orchestration service (deprecation/removal path)
- New/updated payment adapter component (internal boundary)
- Webhook handler/integration endpoint components
- Secrets management and observability deployment slices for payment flows

## Alternatives Considered
### Keep internal orchestrator (rejected)
- Pros: stronger provider abstraction, internal control
- Cons: high maintenance cost, slower product delivery, duplicated vendor capabilities

### Direct Stripe with adapter boundary (selected)
- Pros: faster time-to-market, lower infra/ops burden, still maintains controlled boundary
- Cons: tighter dependency on Stripe features/limits, migration effort, webhook complexity

### Full direct Stripe without boundary (rejected)
- Pros: fastest initial implementation
- Cons: provider details spread across domain code, harder future provider substitution

## Consequences
### Positive
- Reduced ownership of non-differentiating orchestration logic
- Faster adoption of Stripe-native capabilities
- Clearer accountability between domain logic and payment integration boundary

### Negative
- Increased vendor concentration risk
- Need robust webhook idempotency, replay handling, and signature verification
- Migration complexity from legacy orchestration flows

### Neutral
- Some internal operational controls shift from platform code to integration/runbook practices

## Follow-up
- Define adapter interface contract and error taxonomy
- Plan phased migration and decommission strategy for internal orchestrator
- Update model relationships to reflect Stripe integration and webhook flows
- Add runbooks for webhook incidents, retries, and reconciliation
- Review compliance implications and secret/key rotation process
