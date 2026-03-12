Use the standard **external integration** pattern from this workspace.

- Add the payment provider as a dedicated `System_External` element so it is clearly modeled as a third-party dependency.
- Keep the call from your internal API explicit with a typed `-[calls]->` relationship.
- Use a precise action label such as `Process payment`, not something vague like `Uses` or `Talks to provider`.

Example:

```likec4
model {
  payments = System_Existing 'Payments Platform' {
    api = Container_Api 'Payments API' {
      technology 'Node.js, Express'
    }
  }

  paymentProvider = System_External 'Payment Provider' {
    technology 'Stripe'
  }

  payments.api -[calls]-> paymentProvider 'Process payment' {
    technology 'HTTPS'
  }
}
```

That stays consistent with the shared workspace conventions:

- `System_External` already carries the shared external semantics (`#External`)
- `calls` is the standard relationship for synchronous API-to-provider communication
- the relationship label describes the business action, which makes the model much easier to read later

I would avoid modeling the provider as a generic note, unnamed box, or an untyped relationship, because that weakens both consistency and meaning.