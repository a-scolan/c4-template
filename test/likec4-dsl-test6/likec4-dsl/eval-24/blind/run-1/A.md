Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because source, target, and title do not uniquely identify the intended relationship when both typed relationships already exist between the same endpoints with the same title; in this case, omitting the kind does not safely disambiguate the async relationship. `extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it explicitly matches the `sync` relationship, not the existing `async` one.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```