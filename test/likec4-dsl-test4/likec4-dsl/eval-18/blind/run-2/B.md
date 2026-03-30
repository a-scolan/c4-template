No. `extend frontend -> api 'streams' { metadata { qos 'high' } }` does **not** extend the async relationship.

**Why — relationship identity matching**

LikeC4 matches an `extend` target by four fields: source, target, kind, and title. The two existing relationships are:

| | source | target | kind | title |
|---|---|---|---|---|
| R1 | `frontend` | `api` | `async` | `'streams'` |
| R2 | `frontend` | `api` | *(none)* | `'streams'` |

The matcher `extend frontend -> api 'streams'` resolves to source=`frontend`, target=`api`, kind=*(none)*, title=`'streams'`. That identity matches **R2**, not R1. The extend lands on the wrong relationship.

**Ambiguous or wrong?**

Omitting the kind is **wrong** here, not merely ambiguous. Because R2 (the untyped relationship) exists with the same source, target, and title, the matcher is fully resolved — it unambiguously targets R2. LikeC4 has no reason to guess you meant the async one.

**Correct snippet**

Include the kind explicitly to target R1:

```likec4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```

This sets source=`frontend`, target=`api`, kind=`async`, title=`'streams'`, making the identity unique and unambiguous.
