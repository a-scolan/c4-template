No.

For relationship extension matching, LikeC4 identifies a relationship by **source + target + kind**, and adds **title** when needed to distinguish multiple relationships with the same source/target/kind.

Here both relationships have the same:
- source: `frontend`
- target: `api`
- title: `'streams'`

What distinguishes them is the **kind**:
- `frontend -[async]-> api 'streams'`
- `frontend -> api 'streams'`

So `extend frontend -> api 'streams' { ... }` does **not** unambiguously target the async relationship. In this case, omitting the kind is **wrong**, not just loosely ambiguous, because the kind is part of the identity needed to select the typed `async` relationship.

The exact extension snippet that unambiguously targets the async relationship is:

```likec4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```