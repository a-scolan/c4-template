Pattern: **External integration + webhook callback (asynchronous)**.

Model two one-way interactions:
1. Internal API calls Stripe to create payment.
2. Stripe later calls an internal webhook endpoint.

```likec4
stripe = System_External 'Stripe' {
  technology 'HTTPS API'
  description 'External payment platform.'
}

api -[calls]-> stripe 'Creates payment' {
  technology 'HTTPS'
}

paymentWebhook = Container_Api 'Payment Webhook Endpoint' {
  technology 'HTTPS'
  description 'Receives provider payment confirmation callbacks.'
}

stripe -[calls]-> paymentWebhook 'Sends payment confirmation webhook' {
  technology 'HTTPS'
}
```

Important modeling rule:
- Do **not** model this as a synchronous return from Stripe to the original API call path. The webhook is a separate async callback interaction.

Substitutions:
- `parent`: place `paymentWebhook` in the real internal service boundary.
- `exact kinds`: replace element/relationship kinds with declared workspace taxonomy.
- `names`: map to your canonical API and endpoint names.
- `tech`: include actual signature/verification mechanism in description if useful.

If callback ordering/retries matter, capture timing in a dynamic view.