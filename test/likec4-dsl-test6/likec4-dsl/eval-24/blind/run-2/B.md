Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because it omits the relationship kind, so it does not uniquely identify the existing typed relationship you want to extend when multiple typed relationships share the same source, target, and title. `extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it explicitly matches the `sync` relationship, not the existing `async` one.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```