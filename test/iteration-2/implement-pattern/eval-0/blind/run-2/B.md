Pattern: **External integration**.

Recommended LikeC4 starter shape:

```likec4
paymentProvider = System_External 'External Payment Provider' {
  technology 'HTTPS API'
  description 'Third-party payment platform.'
}

internalApi -[calls]-> paymentProvider 'Creates payment request' {
  technology 'HTTPS'
}
```

What to substitute:
- `parent`: put `internalApi` under your real internal system/container hierarchy.
- `exact kinds`: use your declared external-system and relationship kinds if names differ.
- `names`: replace placeholders with canonical identifiers.
- `tech`: include your concrete transport + auth scheme.

Consistency tip: keep payment provider outside your internal boundary and connect through a typed outbound call.