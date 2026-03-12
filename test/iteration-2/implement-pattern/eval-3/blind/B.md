Model this as **two explicit interactions**, not as one request with an implied synchronous return.

A clean LikeC4 structure is:

```likec4
paymentsApi = Container_Api 'Payments API' {
  technology 'Node.js'
}

stripeWebhookEndpoint = Container_Api 'Stripe Webhook Endpoint' {
  technology 'Node.js'
  description 'Receives Stripe payment confirmation webhooks'
}

stripe = System_External 'Stripe' {
  technology 'Payments API'
  #External
}

paymentsApi -[calls]-> stripe 'Create payment' {
  technology 'HTTPS'
}

stripe -[calls]-> stripeWebhookEndpoint 'Send payment confirmation webhook' {
  technology 'HTTPS'
}
```

That keeps the pattern correct:

- `Stripe` is a dedicated `System_External` with the shared `#External` tag.
- The outbound payment creation remains an explicit typed relationship from the internal API to Stripe.
- The webhook is a **second explicit interaction** from Stripe to your internal endpoint.
- It is **not** the return path of the first call.

If you need to show the exact temporal order, retries, or callback sequence in more detail, add a `create-sequence-view` style dynamic view alongside the structural model.
