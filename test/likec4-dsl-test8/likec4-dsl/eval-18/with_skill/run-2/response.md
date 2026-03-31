No. Relationship identity is matched by **source + target + kind**, and **title** is only an extra discriminator when multiple relationships share the same source, target, and kind.

Here, both relationships already share the same source (`frontend`), target (`api`), and title (`'streams'`), but they differ by **kind**:
- `frontend -> api 'streams'` = untyped relationship
- `frontend -[async]-> api 'streams'` = typed `async` relationship

So `extend frontend -> api 'streams' { metadata { qos 'high' } }` does **not** mean “extend the async one”. Omitting the kind is **wrong here**, not just loosely ambiguous, because the kind is part of the relationship identity when a typed relationship exists for that source/target pair. Title alone is not enough to pick the async relationship.

The exact unambiguous extension is:

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```