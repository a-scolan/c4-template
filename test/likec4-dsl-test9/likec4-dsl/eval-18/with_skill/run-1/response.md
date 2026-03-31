No — `extend frontend -> api 'streams' { ... }` does **not** target the async relationship.

LikeC4 matches relationship identity by **source + target + kind + title** (with the title needed when multiple relationships share the same endpoints/kind). Here the two existing relationships are:

- `frontend -> api 'streams'`
- `frontend -[async]-> api 'streams'`

They have the same **source**, **target**, and **title**, but different **kind**:

- untyped/default kind for `frontend -> api 'streams'`
- `async` for `frontend -[async]-> api 'streams'`

So if you omit the kind in the extension matcher, that is **wrong here**, not merely "ambiguous": it matches the **untyped** relationship identity, not the async one. To extend the async relationship, you must include the kind explicitly.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```