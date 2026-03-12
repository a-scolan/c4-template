Suggested ADR file: `ADR/0012-replace-internal-payment-orchestration-with-stripe.md`

# ADR: Replace the internal payment orchestration service with direct Stripe integration via a small internal adapter

## Status
Proposed

## Context
The current architecture uses an internal payment orchestration service. That service adds ownership, maintenance, and operational burden, while much of the required capability now overlaps with Stripe’s managed platform. The team wants to simplify the payment path by integrating directly with Stripe, but still retain a narrow internal adapter boundary so the rest of the system does not depend on raw provider-specific semantics everywhere.

Call out the impacted LikeC4 elements explicitly:
- the internal payment orchestration service being retired or reduced
- the retained internal adapter boundary that will encapsulate Stripe-specific translation
- the external Stripe provider boundary
- upstream callers such as checkout, order, billing, or refund flows
- any views describing payment flows, webhooks, fraud/settlement, or operational ownership

## Decision
Replace the internal payment orchestration service with a direct SaaS integration to Stripe.

Keep a small internal adapter boundary responsible for provider mapping, request/response normalization, idempotency rules, and webhook translation into internal events or commands.

Do not preserve the previous orchestration layer as a general-purpose internal platform unless there is a separately justified architectural reason to do so.

## Consequences

### Positive
- Reduced internal platform surface area and lower maintenance burden
- Faster access to mature Stripe capabilities and provider-managed improvements
- Simpler architecture with fewer internally owned moving parts
- Clearer ownership boundary around a focused adapter instead of a broad orchestration platform

### Negative
- Stronger dependency on a single SaaS provider and its availability, roadmap, and commercial terms
- Reduced control over provider behavior, edge cases, and feature semantics
- Increased exposure to vendor-specific concepts, webhook models, and rate limits
- Future provider switching becomes harder if the adapter boundary is allowed to leak Stripe assumptions

### Follow-up
- Define the migration scope from the old orchestration API to the new adapter boundary
- Design webhook handling, retry behavior, idempotency, and reconciliation flows explicitly
- Update validation and failure-path documentation for payment authorization, capture, refund, and dispute scenarios
- Reassign operational ownership for incident response, credentials, and provider coordination
- Update affected LikeC4 elements and views to show the removed service, retained adapter, and external Stripe boundary
- Consider an `Alternatives Considered` section to capture why “keep the internal orchestrator” was rejected
