# Relationship Identity Matching in `extend` — Async vs Plain

## How LikeC4 identifies a relationship for `extend`

A relationship is identified by the combination of:

1. **Source** element
2. **Target** element
3. **Title** (the string label, e.g. `'streams'`)
4. **Kind** (the relationship kind tag in `[...]`, e.g. `async`; absent means the default/untagged kind)

All four fields together form the identity. When two relationships share the same source, target, and title but differ in kind, they are **distinct** relationships.

---

## Your scenario

```
frontend -[async]-> api 'streams'   // relationship A: kind=async, title='streams'
frontend -> api 'streams'           // relationship B: kind=(default), title='streams'
```

These are two different relationships. They share source (`frontend`), target (`api`), and title (`'streams'`), but differ in kind.

---

## Is `extend frontend -> api 'streams' { ... }` ambiguous or wrong?

It is **wrong (ambiguous leading to incorrect targeting)**: the syntax `frontend -> api 'streams'` omits the kind, which means it matches the relationship with the **default (untagged) kind** — that is, relationship B, not A.

- Omitting `[async]` is **not ambiguous in parsing** — the parser resolves it unambiguously to the default-kind relationship.
- But it is **semantically wrong** for your intent: you want to extend the `async` one (A), but the snippet without `[async]` will extend the untagged one (B).

So the answer is: **No**, you cannot use `extend frontend -> api 'streams' { ... }` to target the async relationship. That snippet will target relationship B instead.

---

## Exact snippet to unambiguously extend the async relationship

```c4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```

Including `[async]` in the extend declaration makes the kind explicit, uniquely identifying relationship A.
