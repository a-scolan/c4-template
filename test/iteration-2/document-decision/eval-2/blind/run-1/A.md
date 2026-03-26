Yes—this is clearly an ADR-level architecture decision. Here is a strong framing.

# ADR: Replace Internal Payment Orchestration with Direct Stripe Integration + Internal Adapter Boundary

## Status
Proposed (or Accepted)

## Context
We currently use an internal payment orchestration service. We plan to simplify by integrating directly with Stripe while keeping a minimal internal adapter boundary to isolate domain logic from provider specifics.

## Decision Drivers
- Reduce platform complexity and maintenance burden
- Improve delivery speed for payment features
- Leverage Stripe’s reliability, compliance, and ecosystem
- Preserve portability via a thin internal abstraction
- Control vendor lock-in risk through bounded integration surface

## Options Considered
1. Keep and evolve internal orchestration service
2. Replace with direct Stripe integration, no boundary
3. Replace with direct Stripe integration, keep thin internal adapter (**chosen**)

## Decision
Adopt **direct Stripe integration** and retain a **small internal adapter boundary** that exposes provider-agnostic payment operations to internal services.

## Rationale
This provides most simplification and time-to-market gains while retaining an intentional seam for testing, policy enforcement, and future provider changes.

## Consequences
### Positive
- Lower operational and ownership overhead
- Faster feature delivery and incident response
- Clearer ownership and reduced duplicated orchestration logic

### Negative / Trade-offs
- Increased dependence on Stripe APIs and roadmap
- Migration effort for existing payment flows
- Need strong idempotency, retries, and webhook handling discipline

## Guardrails
- Keep adapter interface stable and domain-focused
- Centralize Stripe-specific mapping in adapter layer
- Enforce idempotency keys, replay protection, and audit logging
- Define fallback/manual recovery procedures

## Migration Plan (high level)
1. Build adapter and contract tests
2. Migrate one payment flow behind a feature flag
3. Validate operational metrics and failure modes
4. Incrementally migrate remaining flows
5. Decommission orchestration service when parity is proven

## Follow-up
- Run cost/risk review after first production phase
- Revisit multi-provider strategy trigger criteria
- Document operational playbooks and SLOs for payment paths
