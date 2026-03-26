# ADR Framing — Move from Internal Payment Orchestrator to Stripe SaaS + Internal Adapter

## Suggested filename
`ADR/0002-adopt-stripe-saas-with-thin-internal-payment-adapter.md`

## Status
Proposed

## Context
The current internal payment orchestration service is expensive to maintain and slows delivery of payment features. We want to integrate directly with Stripe while preserving a thin internal adapter so the domain remains decoupled from provider-specific APIs.

Main forces:
- Reduce platform maintenance of non-differentiating payment orchestration
- Increase delivery speed for payment features
- Keep a stable internal contract for domain services
- Preserve security/compliance controls and operational observability

## Decision
Integrate directly with Stripe for payment processing and events. Retain a **thin internal payment adapter boundary** as the only contract consumed by domain services.

Not in scope now:
- Multi-provider routing/failover orchestration
- Rebuilding internal orchestration capabilities

## Impacted Elements
- Payment/checkout domain services
- Internal payment orchestrator service (sunset plan)
- Payment adapter component (new or refactored)
- Webhook ingestion and verification component(s)
- Deployment/ops documentation for secrets, retries, reconciliation

## Alternatives Considered
### Keep internal orchestrator
- Pros: internal abstraction and control
- Cons: high cost, duplicated vendor functionality, slower roadmap

### Direct Stripe + thin adapter (**chosen**)
- Pros: lower ops burden, faster feature adoption, boundary preserved
- Cons: provider dependence, migration complexity, webhook operational rigor required

### Direct Stripe without adapter
- Pros: fastest immediate implementation
- Cons: provider coupling leaks into domain code

## Consequences
### Positive
- Faster product iteration on payments
- Reduced internal platform ownership in this area
- Cleaner boundary accountability between domain and integration code

### Negative
- Vendor concentration risk increases
- Higher importance of idempotency/replay protection in webhook handling
- Migration and dual-run complexity during transition

### Neutral
- Some controls shift from internal orchestration logic to contracts/runbooks/monitoring

## Follow-up
- Define adapter interface + error model + retry semantics
- Create phased migration and decommission plan
- Update model relationships to external Stripe and webhook flow
- Add runbooks for reconciliation, incident response, and key rotation
- Confirm compliance controls and audit trail coverage
