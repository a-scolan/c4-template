Pattern: **Payment API + asynchronous webhook callback**.

Represent Stripe integration as two separate one-way relationships.

```likec4
stripe = System_External 'Stripe' {
  technology 'HTTPS API'
  description 'External payment provider.'
}

api -[calls]-> stripe 'Creates payment intent' {
  technology 'HTTPS'
}

webhookEndpoint = Container_Api 'Stripe Webhook Endpoint' {
  technology 'HTTPS'
  description 'Receives Stripe payment confirmation events.'
}

stripe -[calls]-> webhookEndpoint 'Posts payment confirmation webhook' {
  technology 'HTTPS'
}
```

What this avoids:
- It does not imply a synchronous business return from Stripe to the original request path.

Substitutions:
- Use your exact kind names and relationship taxonomy.
- Place `webhookEndpoint` in the correct internal parent.
- Replace placeholders with canonical naming and concrete security details (signature verification, etc.).

If you need retry/order semantics, document them in a dynamic view.