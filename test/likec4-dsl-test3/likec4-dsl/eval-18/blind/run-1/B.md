Not reliably — you should match the original relationship identity as precisely as possible.

For `extend` on relationships, the matcher is based on the relationship identity (source, target, and when present/needed to disambiguate, kind and title). Since the original is:

`frontend -[async]-> api 'streams'`

the safest/correct extension is to include the same kind (and title):

```likec4
model {
  extend frontend -[async]-> api 'streams' {
    metadata { qos 'high' }
  }
}
```

Using `extend frontend -> api 'streams'` may fail or become ambiguous if there are multiple relationships between `frontend` and `api` (different kinds/titles).