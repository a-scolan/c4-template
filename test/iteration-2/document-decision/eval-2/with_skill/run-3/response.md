# ADR Framing — Retire Internal Payment Orchestrator; Integrate Stripe Directly via Thin Adapter

## Suggested filename
`ADR/0002-retire-internal-payment-orchestrator-adopt-stripe-with-adapter.md`

## Status
Proposed

## Context
An internal payment orchestration service currently mediates payment provider interactions. It increases maintenance overhead and slows product evolution. The target state is direct Stripe integration while preserving a constrained internal adapter boundary to keep domain code insulated from provider details.

Decision forces:
- Reduce maintenance of non-core platform capabilities
- Accelerate delivery of payment features
- Maintain stable internal domain contract
- Respect security/compliance obligations and operational reliability

## Decision
Use Stripe SaaS directly for payment operations and events. Keep a **small internal adapter** as the domain-facing boundary.

Out of scope:
- Building a broad multi-PSP orchestration platform now
- Eliminating the boundary and coupling domain logic to Stripe SDK/API details

## Impacted Elements
- Checkout/payment domain services
- Internal payment orchestrator (deprecation and removal)
- Payment adapter boundary component and contracts
- Webhook verification/processing path
- Deployment/operations controls: secrets, retries, reconciliation, alerting

## Alternatives Considered
### Continue internal orchestration
- Pros: centralized abstraction/control
- Cons: high ownership cost and slower change velocity

### Direct Stripe + thin adapter (selected)
- Pros: faster delivery, less infra burden, controlled internal contract
- Cons: stronger provider dependency, migration and webhook complexity

### Direct Stripe with no adapter
- Pros: shortest path initially
- Cons: provider coupling leaks into domain and makes future substitution harder

## Consequences
### Positive
- Faster integration of payment capabilities
- Lower maintenance burden for orchestration logic
- Better architectural clarity around payment boundary ownership

### Negative
- Vendor lock-in pressure increases
- Must engineer robust idempotency, retries, and replay protection
- Migration requires careful cutover and reconciliation handling

### Neutral
- Some operational safeguards move from platform code into process/runbooks/monitoring

## Follow-up
- Define adapter contract and canonical error mapping
- Plan phased migration and decommission milestones
- Update model elements/relationships for Stripe + webhook flows
- Add runbooks for incident handling and reconciliation
- Validate compliance impact and key/secret lifecycle controls
