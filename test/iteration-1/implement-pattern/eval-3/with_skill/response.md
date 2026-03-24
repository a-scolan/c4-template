Pattern: External integration plus webhook callback, modeled as two separate one-way relationships.

Minimal scaffold:
stripe = System_External 'Stripe' {
  technology 'HTTPS API'
  description 'External payment provider.'
}

api -[calls]-> stripe 'Creates payment' {
  technology 'HTTPS'
}

stripe -[calls]-> api 'Sends payment confirmation webhook' {
  technology 'HTTPS webhook'
}

How to keep it accurate:
- Treat the webhook as a second independent inbound call, not as a return arrow on the create-payment request.
- If the receiving endpoint deserves its own element, split it out under `api` using the exact declared kind from your workspace.

Substitute before finalizing:
- parent: place `stripe` as an external system and the receiving endpoint under your internal API boundary
- exact kinds: replace `System_External`, `api`, or `calls` with the exact declared names if needed
- names: use the real payment API and webhook endpoint names
- tech: typically `HTTPS` for the outbound payment call and `HTTPS webhook` for the callback

If you need to show the order explicitly, move that temporal story to a dynamic or sequence view instead of turning the first call into a synchronous round trip.
