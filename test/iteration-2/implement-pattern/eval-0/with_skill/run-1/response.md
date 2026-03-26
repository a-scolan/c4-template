Pattern: **External integration**.

Use one internal API element and one external system element, then connect them with a typed call.

```likec4
paymentProvider = System_External 'Payment Provider' {
  technology 'HTTPS API'
  description 'Third-party payment service.'
}

internalApi -[calls]-> paymentProvider 'Creates payment' {
  technology 'HTTPS'
}
```

Substitutions to apply in your workspace:
- `parent`: place `internalApi` under your real internal system/container parent.
- `exact kinds`: replace `System_External` and `calls` only if your spec defines stricter names.
- `names`: swap `paymentProvider`/`internalApi` with your canonical identifiers.
- `tech`: set concrete protocol/auth details (e.g., HTTPS + OAuth2/API key).

Consistency rule: keep the provider modeled as external boundary, not as an internal container.