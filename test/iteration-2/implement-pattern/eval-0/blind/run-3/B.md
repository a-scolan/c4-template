Pattern: **Internal API to external payment provider** (external integration pattern).

Minimal consistent scaffold:

```likec4
paymentProvider = System_External 'Payment Provider' {
  technology 'HTTPS API'
  description 'External provider used for payment authorization and capture.'
}

api -[calls]-> paymentProvider 'Creates payment' {
  technology 'HTTPS'
}
```

Substitute before finalizing:
- `parent`: ensure `api` sits in your real internal hierarchy.
- `exact kinds`: match declared workspace element and relationship types.
- `names`: use canonical element identifiers.
- `tech`: specify concrete protocol/auth details.

Keep the provider external to preserve boundary clarity and dependency direction.