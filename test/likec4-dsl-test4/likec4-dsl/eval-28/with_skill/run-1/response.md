Wrong: extend frontend -> api 'streams'

When two relationships share the same source (`frontend`), target (`api`), and title (`'streams'`) but differ in kind — one is `async`, the other is untyped — omitting the kind leaves the matcher ambiguous: LikeC4 cannot determine which of the two relationships to extend, because relationship identity is resolved by source + target + kind + title together. Without the kind, both relationships match on the remaining three fields, so the extension is invalid.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```
