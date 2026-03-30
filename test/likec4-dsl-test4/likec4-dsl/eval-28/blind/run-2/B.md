Wrong: extend frontend -> api 'streams'

When two relationships share the same source, target, and title but differ in kind, the kind is part of a relationship's identity in LikeC4. Using `extend frontend -> api 'streams'` (without any kind) matches only the **untyped** relationship — the one defined with plain `->` — and does not target the `async`-kinded relationship at all. It is not ambiguous between the two; it simply selects the wrong one. To unambiguously target the async relationship, you must include the kind in the extend matcher.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```
