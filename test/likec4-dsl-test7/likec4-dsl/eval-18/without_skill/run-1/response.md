No — not if your goal is to extend the `async` relationship.

Relationship extension matching is by identity: **source + target + title + kind**.

You have two relationships with the same source/target/title:
- `frontend -[async]-> api 'streams'`
- `frontend -> api 'streams'` (non-async/default kind)

So `extend frontend -> api 'streams' { ... }` omits the kind and therefore does **not** uniquely point to the async one. Here, omitting kind is **wrong** for that intent (and ambiguous from a reader-intent perspective), because kind is part of identity and distinguishes these two relationships.

Use this exact unambiguous snippet:

`extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}`
