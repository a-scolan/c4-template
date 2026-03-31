Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because the matcher is missing the relationship kind. Here, both `frontend -[async]-> api 'streams'` and `frontend -[sync]-> api 'streams'` already exist, so source + target + title alone do not uniquely identify the intended relationship. In this case, the kind is required for exact matching.

`extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it explicitly selects the `sync` relationship, not the existing `async` one you want to extend.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { channel 'realtime' }
}
```