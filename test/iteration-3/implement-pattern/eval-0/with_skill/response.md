Use the External integration pattern.

Minimal scaffold:
paymentProvider = System_External 'Payment Provider' {
  technology 'HTTPS API'
}

api -[calls]-> paymentProvider 'Create payment' {
  technology 'HTTPS'
}

Why this is consistent in this workspace:
- `System_External` is the valid external system kind here, and it already carries the shared `#External` tag.
- `calls` is the correct typed relationship for a synchronous API call.
- Use an explicit action label such as 'Create payment' or 'Capture payment', not a vague label like 'Uses'.

Substitute:
- `api`: your existing internal API element, typically a `Container_Api`
- `paymentProvider`: the real provider name, for example `Stripe`
- parent, names, and technologies to match your current model
