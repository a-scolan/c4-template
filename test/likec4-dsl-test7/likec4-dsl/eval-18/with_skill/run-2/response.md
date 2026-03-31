No.

`extend frontend -> api 'streams' { ... }` does **not** unambiguously target the async relationship here. Relationship identity matching is based on **source + target + kind (+ title when needed)**.

In your case, these two relationships already exist:

- `frontend -> api 'streams'`
- `frontend -[async]-> api 'streams'`

They have the same **source**, **target**, and **title**, but different **kind**. That means omitting the kind is **wrong here**, not merely ambiguous, because it can match the unkinded relationship instead of the typed async one.

The exact extension snippet that unambiguously targets the async relationship is:

```likec4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```