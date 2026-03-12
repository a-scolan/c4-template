Add a dedicated external system for the payment provider and keep it clearly marked as third-party.

```likec4
paymentProvider = System_External 'Payment Provider' {
  technology 'Stripe / Adyen / PSP API'
  description 'Third-party payment platform'
}

vault.api -[calls]-> paymentProvider 'Process payment'
```

Use `System_External` so the provider is modeled as a separate external dependency, and keep the shared external tag that comes with that element kind. For the relationship, use a typed `calls` link from `vault.api` to the provider with an explicit action label such as `Process payment`, `Authorize payment`, or `Capture payment`.

Avoid vague labels like `Integrates with` or `Uses`, because they hide the business action.