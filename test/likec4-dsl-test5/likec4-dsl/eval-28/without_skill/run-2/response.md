Wrong: extend frontend -> api 'streams'

Omitting the relationship kind is wrong here because there are two distinct relationships with the same source, target, and title (`async` and default), so the extension must include `-[async]->` to disambiguate and target the correct edge.

```c4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```Wrong: extend frontend -> api 'streams'

When both `frontend -[async]-> api 'streams'` and `frontend -> api 'streams'` coexist, the two relationships are distinct: one carries the `async` kind and one is untyped. Writing `extend frontend -> api 'streams'` matches only the untyped relationship, so any metadata added would be applied to the wrong relationship — the `async` one would remain unmodified. The relationship kind is part of the identity key used to resolve which relationship to extend, so omitting it when an explicit-kind variant exists silently targets the wrong entry instead of raising an error.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```
