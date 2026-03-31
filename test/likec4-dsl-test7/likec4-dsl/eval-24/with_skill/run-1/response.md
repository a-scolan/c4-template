Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because both `frontend -[async]-> api 'streams'` and `frontend -[sync]-> api 'streams'` already exist. Relationship extension matching is based on source + target + kind (+ title when needed). Omitting the kind does not uniquely identify the async relationship here, so it is not specific enough for this case.

`extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it explicitly matches the `sync` relationship, not the `async` one.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```