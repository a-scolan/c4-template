Wrong: extend frontend -> api 'streams'

When both `frontend -[async]-> api 'streams'` and `frontend -> api 'streams'` exist, omitting the relationship kind in the `extend` expression is ambiguous — LikeC4 cannot determine which of the two distinct relationships (the typed `async` one vs. the untyped one) you intend to augment. The kind is part of the relationship's identity, so without it the compiler cannot resolve the target uniquely and will either raise an error or silently target the wrong relationship.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```
