# Response — eval-2, without_skill, run 2

## Prompt

We are replacing an internal payment orchestration service with a direct SaaS integration to Stripe, keeping only a small internal adapter boundary. This is a real architecture decision. Help me frame the ADR.

## Response

Here's an ADR framing for migrating from internal payment orchestration to Stripe:

---

**ADR-NNN: Integrate Stripe as the Payment Provider, Replacing Internal Orchestration**

**Status:** Accepted

**Context:**

The system has been running a custom internal payment orchestration service responsible for:
- Payment lifecycle management (initiation, capture, refund)
- Webhook handling for async payment events
- Retry and idempotency logic
- Provider abstraction (multi-provider routing)

Maintaining this service requires ongoing effort in compliance (PCI-DSS), reliability engineering, and payment domain expertise. Stripe provides a battle-tested, PCI-compliant SaaS that covers these concerns natively.

The team decided to evaluate a migration to direct Stripe integration.

**Alternatives Considered:**

| Option | Notes |
|--------|-------|
| Keep internal service | High maintenance cost, compliance burden |
| Stripe (full integration) | Preferred – offloads orchestration, compliance |
| Another SaaS (Adyen, Braintree) | Stripe selected for team familiarity and feature set |

**Decision:**

Adopt **Stripe** as the primary payment provider via SaaS integration, encapsulated behind a thin internal adapter boundary.

The adapter:
- Exposes a domain-neutral interface (`PaymentGateway`)
- Translates domain events into Stripe API calls
- Isolates Stripe-specific error codes and webhook signatures

**Consequences:**

*Positive:*
- Reduced maintenance: no internal orchestration logic to maintain
- Stripe handles PCI-DSS L1 compliance
- Native support for subscriptions, invoicing, fraud detection
- Faster feature delivery using Stripe Dashboard and APIs

*Negative:*
- External dependency: Stripe downtime impacts payments
- Stripe pricing model introduces variable transaction costs
- The adapter must be kept thin to avoid rebuilding abstraction over abstraction

---

File as `ADR-NNN-stripe-payment-integration.md` in your project's ADR folder.
