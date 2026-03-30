# Relationship Identity Matching and `extend` Ambiguity

## Background: How relationship identity works in LikeC4

A relationship in LikeC4 is identified by the combination of:
- **source** element
- **target** element
- **kind** (optional — defaults to the implicit/untyped relationship when omitted)
- **title** (optional label)

When using `extend` to augment an existing relationship (e.g., add metadata), LikeC4 must match the `extend` declaration against exactly one existing relationship. The match is performed on source + target + kind + title.

---

## The two existing relationships

```c4
frontend -[async]-> api 'streams'   // kind=async, title='streams'
frontend -> api 'streams'            // kind=(none/default), title='streams'
```

These are **two distinct relationships** because they differ in `kind`: one is `async`, the other has no kind (the implicit default).

---

## Is `extend frontend -> api 'streams' { ... }` ambiguous or wrong?

```c4
extend frontend -> api 'streams' {
  metadata { qos 'high' }
}
```

The `->` syntax (without a kind in `[...]`) matches the **untyped / default-kind** relationship. Therefore:

- It is **not ambiguous** — it is **wrong for the intended target**.
- It unambiguously matches `frontend -> api 'streams'` (the untyped one), **not** `frontend -[async]-> api 'streams'`.

Omitting the kind is not syntactically ambiguous (the parser resolves it to the default/untyped kind), but it is **semantically incorrect** if your intent is to extend the `async` relationship. You will silently extend the wrong relationship.

---

## Exact extension snippet that unambiguously targets the async relationship

```c4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```

By including `-[async]->`, the kind is explicit and the match is unambiguous: only `frontend -[async]-> api 'streams'` satisfies all four identity components (source=`frontend`, target=`api`, kind=`async`, title=`'streams'`).
