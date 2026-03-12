Suggested ADR file: `ADR/0002-replace-internal-payment-orchestrator-with-stripe-adapter.md`

## Status

Proposed

## Context

We are replacing an internal payment orchestration service with a direct SaaS integration to Stripe, while retaining a small internal adapter boundary. This is a real architecture decision because it changes system structure, ownership boundaries, integration responsibilities, and operational risk.

The ADR should name the impacted LikeC4 elements explicitly:
- the internal payment orchestration service that will be removed or decommissioned
- the remaining internal payment adapter/boundary that will isolate the rest of the system from Stripe specifics
- the external Stripe provider boundary and its relationships to internal services
- any calling services, checkout flows, or payment-related views that currently depend on the orchestration layer

Key forces to describe:
- desire to reduce internally owned payment orchestration complexity
- need for faster delivery by using a mature SaaS capability
- requirement to keep a controlled internal boundary so Stripe details do not leak everywhere
- compliance, operational, and failure-mode implications of relying more directly on an external provider

## Decision

Replace the internal payment orchestration service with a direct integration to Stripe, while keeping a minimal internal adapter that provides a stable internal contract.

The ADR should state that:
- the orchestration service is being retired as a primary architectural element
- the internal adapter remains as the only internal boundary exposed to the rest of the platform
- Stripe becomes the main external payment capability provider
- LikeC4 model elements and views must be updated to show the removed internal service, the retained adapter, and the external provider relationship

Rationale to capture:
- use Stripe’s managed capabilities instead of continuing to build and operate duplicated internal orchestration logic
- preserve some internal decoupling through the adapter so the system is not fully hard-wired to provider-specific APIs

## Consequences

### Positive Consequences
- Reduced internal platform complexity and less custom orchestration code to maintain
- Faster access to mature SaaS payment features and ecosystem support
- Clearer ownership boundary if the internal adapter becomes the single integration contract for internal callers
- Potentially lower delivery time for payment enhancements

### Negative Consequences
- Increased dependency on Stripe availability, API behavior, and commercial terms
- Reduced control over some orchestration behavior and provider-specific edge cases
- Risk of vendor lock-in if the internal adapter is kept too thin or leaks Stripe semantics
- New exposure to webhook reliability, idempotency, reconciliation, and provider-driven lifecycle events

### Neutral Consequences
- Existing payment-related views, relationships, and element descriptions will need to be updated
- Team responsibilities may shift from operating an internal orchestration service to managing provider integration quality and contract stability

Important follow-up implications to include in the ADR:
- migration scope for existing payment flows and any in-flight transactions
- webhook handling design, retries, signatures, and event reconciliation
- validation and error-mapping changes at the internal adapter boundary
- operational ownership for provider incidents, monitoring, secrets, rate limits, and support escalation
- decommissioning plan for the retired orchestration service, including data, dashboards, and runbooks
