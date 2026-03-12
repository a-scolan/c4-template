You can frame the ADR like this.

Suggested file: `ADR/0002-replace-payments-service-with-stripe-integration.md`

# ADR-0002: Replace `payments-service` with direct Stripe integration via `stripeAdapter`

## Status

Proposed

## Context

The current architecture uses an internal `payments-service` to manage payment workflows. We are considering replacing that service with a direct SaaS integration to Stripe while keeping a small `stripeAdapter` inside our system boundary.

Key drivers:
- Reduce the operational burden of owning and maintaining a dedicated internal payment service.
- Use Stripe’s mature capabilities for payment flows, compliance support, and ecosystem integrations.
- Keep a thin internal abstraction so the rest of the system does not couple directly to Stripe-specific API details.
- Make the architectural change explicit because it affects responsibilities, dependencies, and control boundaries.

Impacted model elements:
- `payments-service`
- `stripeAdapter`
- Any application or API elements that currently call `payments-service`
- The external Stripe integration point, if modeled explicitly

## Decision

Retire the internal `payments-service` and replace it with a direct integration to Stripe, mediated by a small internal `stripeAdapter`.

Rationale:
- Stripe provides a well-supported SaaS platform for payment capabilities that we do not want to build and operate ourselves.
- A thin `stripeAdapter` preserves a local seam for request mapping, error handling, webhook coordination, retries, and limited future change isolation.
- This shifts the architecture from service ownership to vendor integration while keeping the rest of the system protected from raw provider-specific details.

## Consequences

### Positive Consequences
- Reduced maintenance and operational load by removing an internal payment service.
- Faster adoption of mature payment features already available in Stripe.
- Potentially improved reliability, compliance posture, and ecosystem support.
- Clearer separation between core business logic and payment-provider integration concerns.

### Negative Consequences
- Increased dependency on a third-party SaaS provider.
- Reduced control over payment-domain behavior compared with a fully internal service.
- Exposure to vendor pricing changes, API evolution, rate limits, and service outages.
- Migration effort is required for flows, webhooks, error handling, observability, and rollback planning.
- The `stripeAdapter` can grow into an accidental mini-service if its scope is not tightly controlled.

### Neutral Consequences
- Some existing call paths will be redirected from `payments-service` to `stripeAdapter`.
- Architecture documentation and LikeC4 relationships will need updating to show the new dependency structure.
- Operational responsibility moves from running a service to managing a vendor integration.

## Notes

### Related Elements
- `payments-service`
- `stripeAdapter`
- Stripe as an external system, if represented in the model

### Follow-up Topics
- Webhook handling and idempotency strategy
- Retry and failure-mode design
- PCI/compliance boundaries
- Exit strategy if provider replacement is needed later
