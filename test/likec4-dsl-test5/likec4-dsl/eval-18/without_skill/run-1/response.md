No — not for the async relationship.

Relationship identity matching uses **source + target + title + kind**. Since you have both `frontend -[async]-> api 'streams'` and `frontend -> api 'streams'`, omitting the kind does not uniquely express the async one; here it is wrong for that intent.

Use this exact extension to unambiguously target the async relationship:

```likec4
extend frontend -[async]-> api 'streams' {
    metadata {
        qos 'high'
    }
}
```
# Relationship Identity Matching in LikeC4 `extend`

## The Two Relationships

```likec4
frontend -[async]-> api 'streams'   // kind=async,  title='streams'
frontend -> api          'streams'  // kind=(none),  title='streams'
```

## Why `extend frontend -> api 'streams' { ... }` Does NOT Target the Async Relationship

In LikeC4, a relationship's **identity** is composed of four fields:

| Field  | Role in matching |
|--------|-----------------|
| source | required         |
| target | required         |
| title  | part of identity |
| kind   | part of identity |

Two relationships are distinct when **any** of these fields differ. In the example above, both relationships share the same source (`frontend`), target (`api`), and title (`'streams'`), but differ in **kind** (`async` vs. no kind). They are therefore two separate, non-overlapping relationships.

The `extend` keyword resolves which relationship to patch by performing the same four-field identity match. The syntax:

```likec4
extend frontend -> api 'streams' { ... }
```

uses the **plain arrow** `->`, which means kind = *(none / default)*. This unambiguously matches the **second** relationship (the one without a kind), not the async one.

## Is Omitting the Kind Ambiguous or Wrong?

**It is wrong, not merely ambiguous.**

Because there are no two relationships with exactly the same (source, target, title, kind) tuple, every extend expression resolves to exactly one relationship (or zero, if no match exists). Omitting the kind is not ambiguous — the resolver picks the no-kind relationship with certainty. The problem is that it picks the *wrong* one for the stated goal. The async relationship is silently left unmodified.

## Exact Snippet to Unambiguously Target the Async Relationship

Include the kind in the arrow syntax:

```likec4
extend frontend -[async]-> api 'streams' {
    metadata {
        qos 'high'
    }
}
```

This matches (source=`frontend`, target=`api`, title=`'streams'`, kind=`async`) — the precise identity of the first relationship — and applies the metadata patch to it alone.
