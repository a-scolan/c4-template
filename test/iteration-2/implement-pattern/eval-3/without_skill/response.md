Model this as **two separate interactions**, not one request with an implied return.

1. Your internal API calls Stripe to create the payment.
2. Stripe later calls your internal webhook endpoint with the confirmation.

Use a dedicated external system for Stripe and keep both flows explicit:

```likec4
model {
  billing = System_Existing 'Billing Platform' {
    paymentsApi = Container_Api 'Payments API' {
      technology 'Node.js'
    }

    webhookEndpoint = Container_Api 'Stripe Webhook Endpoint' {
      technology 'Node.js'
    }
  }

  stripe = System_External 'Stripe' {
    technology 'Stripe Payments'
  }

  billing.paymentsApi -[calls]-> stripe 'Create payment' {
    technology 'HTTPS'
  }

  stripe -[calls]-> billing.webhookEndpoint 'Send payment confirmation webhook' {
    technology 'HTTPS'
  }
}
```

Why this is the right pattern:

- `System_External` gives Stripe the shared external semantics (`#External`)
- the outbound payment creation call stays an explicit typed relationship
- the webhook is modeled as a **second explicit interaction**, not as the “response” of the first arrow

That distinction matters because the webhook is asynchronous from a modeling point of view, even if it also uses HTTPS.

If you need to show the detailed temporal order more precisely, a sequence view can complement the static model nicely; the structural model should still keep the outbound call and inbound webhook as two separate relationships.