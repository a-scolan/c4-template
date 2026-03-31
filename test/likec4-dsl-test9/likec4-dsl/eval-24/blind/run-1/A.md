Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because relationship identity here must include the kind: both relationships have the same source, target, and title, so omitting `-[async]->` does not uniquely identify the async relationship.

`extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it explicitly matches the sync edge, not the async one.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```
