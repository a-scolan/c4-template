**What `*` includes in a scoped view (`view backend of cloud.backend { include * }`):**

From `references/predicates.md` — Wildcard expression semantics:
> *If used inside a scoped view, it selects the scoped element, its direct children, and all relationships with them.*

So `*` includes:
1. `cloud.backend` itself
2. Its **direct children** only (e.g., `cloud.backend.api`, `cloud.backend.db`)
3. All **relationships between** those elements (internal only)

It does **NOT** include the whole model, ancestors, deployment nodes, or any external elements that happen to have a relationship with `cloud.backend`.

---

**Minimal snippet adding only incoming and outgoing neighbors:**

```likec4
view backend of cloud.backend {
    include *                   // cloud.backend + direct children + internal relationships
    include -> cloud.backend -> // any relationships between cloud.backend and the rest of the model (both directions)
}
```

The `-> <expr> ->` predicate (`-> cloud.backend ->`) means *"any relationships between the element selected by `expr` and the accumulated result"* (bidirectional). After `include *` has placed `cloud.backend` and its children in the accumulated result, this second rule brings in:
- Every element that has a relationship **pointing to** `cloud.backend` (incomers), plus those incoming relationships
- Every element that `cloud.backend` has a relationship **pointing to** (outgoers), plus those outgoing relationships

This pattern is confirmed by the canonical example in `references/examples.md`:
```likec4
// "of" scopes the view — `*` means the scoped element + direct children
view backend of cloud.backend {
    include *
    include -> cloud.backend ->  // incoming/outgoing relations
    ...
}
```
