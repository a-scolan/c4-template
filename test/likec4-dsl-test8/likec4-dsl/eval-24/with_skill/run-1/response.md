Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because relationship extension matching here must include the relationship kind when multiple typed relationships exist between the same source and target. Both edges share the same source, target, and title, so omitting `-[async]->` does not uniquely identify the intended relationship.

`extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it matches the `sync` edge, not the existing `async` edge you want to extend.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata {
    note 'extends the async streams relationship'
  }
}
```