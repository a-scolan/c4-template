Wrong: extend frontend -> api 'streams'

When both `frontend -[async]-> api 'streams'` and `frontend -> api 'streams'` exist between the same two elements, the relationship kind (`async`) is part of what uniquely identifies a relationship. Using `extend frontend -> api 'streams'` without the kind is ambiguous — the model cannot determine which of the two relationships to extend, and will either target the wrong one or produce a resolution error. You must include the kind to unambiguously select the intended relationship.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```
