Pattern: **Stripe outbound call plus asynchronous inbound webhook**.

Use two distinct interactions rather than one request/response chain.

```likec4
stripe = System_External 'Stripe' {
  technology 'HTTPS API'
  description 'External payment processor.'
}

api -[calls]-> stripe 'Creates payment' {
  technology 'HTTPS'
}

stripeWebhookEndpoint = Container_Api 'Stripe Webhook Endpoint' {
  technology 'HTTPS'
  description 'Receives Stripe event callbacks (payment confirmation, etc.).'
}

stripe -[calls]-> stripeWebhookEndpoint 'Sends webhook event' {
  technology 'HTTPS'
}
```

Avoid this modeling error:
- Don’t imply synchronous business confirmation coming back through the initial API call arrow. The webhook is a separate asynchronous callback.

Substitutions:
- Align element kinds, relationship kinds, and names with your workspace declarations.
- Place webhook endpoint under the correct internal service parent.
- Add security detail (signature verification/idempotency) in description as needed.

If sequence timing (retries/order) is important, document it in a dynamic view.