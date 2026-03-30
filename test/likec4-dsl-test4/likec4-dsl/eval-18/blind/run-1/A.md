# Eval 18 — Extending the async relationship unambiguously

## Can I use `extend frontend -> api 'streams' { ... }` to target the async one?

**No.** Using that form is **ambiguous**, not merely wrong syntax.

### Relationship identity matching

LikeC4 matches an `extend` target by comparing four fields:

| Field  | Role                                       |
|--------|--------------------------------------------|
| source | Always required                            |
| target | Always required                            |
| title  | Used to narrow when multiple relations exist |
| kind   | Used to narrow when multiple relations exist |

Given the two existing relationships:

```likec4
frontend -[async]-> api 'streams'   // kind=async, title='streams'
frontend -> api 'streams'           // kind=(none), title='streams'
```

Both share the same source (`frontend`), target (`api`), and title (`'streams'`). The **only distinguishing field is the kind**. `extend frontend -> api 'streams' { ... }` omits the kind, so the matcher cannot resolve which of the two relationships to extend — this is **ambiguous**.

### Is omitting the kind ambiguous or wrong?

It is **ambiguous**. If only one relationship existed between `frontend` and `api` with title `'streams'`, omitting the kind would be fine. Here, because two relationships share all other identity fields, the kind is the required disambiguator. Omitting it leaves the matcher with two equally valid candidates.

### Exact extension that unambiguously targets the async relationship

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```

Including `-[async]->` pins the identity to the relationship whose kind is `async`, making the match unambiguous.
