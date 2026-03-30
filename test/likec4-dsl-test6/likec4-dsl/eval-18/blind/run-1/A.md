No — that extension does **not** target the async relationship.

Relationship identity matching uses **source + target + title + kind**. With both `frontend -[async]-> api 'streams'` and `frontend -> api 'streams'` present, omitting the kind in `extend frontend -> api 'streams' ...` matches the non-async (`->`) relationship. So omitting kind here is **wrong for your intent**, not merely stylistic.

Use this exact extension to unambiguously target the async one:

```likec4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```