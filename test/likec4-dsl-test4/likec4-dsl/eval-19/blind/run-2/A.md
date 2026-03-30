# Scoped `include *` semantics

- **Base include set.** In a scoped view (`of cloud.backend`), `*` selects `cloud.backend` itself, its **direct children** (one level deep — not grandchildren or deeper), and all relationships among those elements.

- **What else can become visible.** Because including a relationship always pulls in both its source and target, any element outside `cloud.backend` that shares a relationship with `cloud.backend` or one of its direct children is implicitly added to the view as a neighbor endpoint — along with that connecting relationship. These external neighbours are not selected by `*`; they appear only as implicit side-effects of a matched relationship.

## Minimal snippet

```likec4
view backend of cloud.backend {
  include *
  include * -> cloud.backend
  include cloud.backend -> *
}
```

- `include *` — scoped element + direct children + their internal relationships.
- `include * -> cloud.backend` — all incoming relationships from any model element to `cloud.backend`, plus the source elements.
- `include cloud.backend -> *` — all outgoing relationships from `cloud.backend` to any model element, plus the target elements.
