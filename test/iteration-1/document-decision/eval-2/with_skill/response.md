Use `ADR/0002-replace-payments-service-with-stripe.md`

# ADR-0002: Replace `payments-service` with a direct Stripe integration

## Status
Proposed

## Context
The current architecture routes payment processing through the internal `payments-service`. That gives us full control, but it also creates ongoing operational and maintenance overhead for provider-specific APIs, retries, webhooks, reconciliation, and security-sensitive payment concerns. We now want to simplify the architecture by removing the internal service and keeping only a small `stripeAdapter` that isolates Stripe-specific logic from the rest of the system. This decision affects the LikeC4 elements `payments-service` and `stripeAdapter`, plus any internal callers that currently depend on `payments-service`.

## Decision
Retire the internal `payments-service` and integrate directly with Stripe through a thin `stripeAdapter`. The `stripeAdapter` will be the only internal boundary responsible for Stripe request mapping, webhook verification, idempotency handling, and translation between Stripe concepts and our internal domain model.

## Consequences

### Positive
- Reduces platform surface area by removing a full internal payment service.
- Shifts commodity payment capabilities to Stripe, including managed payment features and provider expertise.
- Lowers maintenance burden for payment orchestration, retries, and provider-specific behavior.
- Keeps Stripe-specific logic isolated in `stripeAdapter` instead of spreading it across the system.

### Negative
- Introduces stronger dependency on a SaaS provider for a critical business capability.
- Reduces control over payment flow behavior, data shape, and change timing compared with a fully owned internal service.
- Makes Stripe API changes, outages, rate limits, and webhook delays part of our runtime risk profile.
- Requires careful migration planning for contracts, idempotency, reconciliation, and historical payment handling.