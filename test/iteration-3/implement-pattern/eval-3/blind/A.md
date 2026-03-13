Use the External integration pattern, but model the outbound payment call and the inbound webhook as two separate interactions.

Minimal scaffold:
stripe = System_External 'Stripe' {
  technology 'HTTPS API'
}

api -[calls]-> stripe 'Create payment' {
  technology 'HTTPS'
}

stripe -[calls]-> api 'Send payment confirmation webhook' {
  technology 'HTTPS'
}

Why this is the right shape:
- `System_External` is the correct external provider kind here and already applies the shared `#External` tag.
- The initial payment request is an explicit typed `calls` relationship from the internal API to Stripe.
- The webhook is a second explicit interaction initiated by Stripe back to your internal endpoint; it is not the return arrow of the first relationship.
- If the webhook lands on a dedicated internal endpoint, split that endpoint into its own `Container_Api`; otherwise reusing `api` is a fine starter scaffold.

If detailed timing, retries, signature validation, or callback order matter, complement this structural model with `create-sequence-view`.

Substitute:
- your exact internal API or webhook endpoint name
- concrete action labels such as 'Create payment intent' and 'Confirm payment via webhook'
- parent, names, and technologies to match the repository model
