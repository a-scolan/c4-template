# Response — eval-2, without_skill, run 3

## Prompt

We are replacing an internal payment orchestration service with a direct SaaS integration to Stripe, keeping only a small internal adapter boundary. This is a real architecture decision. Help me frame the ADR.

## Response

Good — replacing an internal service with a SaaS platform is exactly the kind of decision that benefits from a documented ADR. Here's a proposed structure:

---

**ADR-NNN: Replace Internal Payment Orchestration Service with Stripe**

**Status:** Accepted

**Context:**

The current architecture includes a bespoke payment orchestration service that manages the end-to-end payment lifecycle. This service was initially built to support multi-provider flexibility but has since become a maintenance liability:

- High compliance overhead (PCI-DSS scope spans internal infrastructure)
- Fragile retry and webhook processing logic
- Limited team capacity to extend payment features

Stripe is a mature payment infrastructure platform offering compliant, reliable payment orchestration as a managed service. The migration would reduce scope and operational risk while maintaining a thin adapter boundary that insulates domain logic from provider specifics.

**Decision:**

We will decommission the internal payment orchestration service and integrate directly with **Stripe** as the payment provider. A lightweight internal `PaymentGateway` adapter will translate domain operations to Stripe API calls, keeping Stripe-specifics contained.

The adapter boundary must remain minimal:
- No business logic inside the adapter
- No internal retry orchestration that duplicates what Stripe handles
- Domain events mapped — not duplicated — from Stripe webhooks

**Consequences:**

*Positive:*
- PCI-DSS compliance delegated to Stripe (certified L1 provider)
- Operational complexity of payment retries, idempotency, and event sourcing offloaded
- Access to Stripe-native features (Radar fraud detection, billing portal, Connect)
- Internal service retired, reducing surface area to maintain

*Negative:*
- Dependency on Stripe's uptime and API stability
- Transaction fees as a variable cost (previously CAPEX)
- If payment provider needs to change, adapter refactoring is required
- Webhook delivery is eventually consistent — code must handle out-of-order events

*Mitigation:*
- Monitor Stripe status actively in runbooks
- Design adapter interface to be provider-agnostic enough for future substitution
- Test webhook delivery idempotency thoroughly before rollout

---

File as `ADR-NNN-replace-payment-service-with-stripe.md`. Adjust ADR number to your sequence.
