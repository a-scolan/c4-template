No.

Relationship extension matching is by identity (source, target, title, and kind when present). Since both `frontend -[async]-> api 'streams'` and `frontend -> api 'streams'` exist, omitting the kind here is **wrong** (not just ambiguous), because it can match the unkinded relationship instead of the async one.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```