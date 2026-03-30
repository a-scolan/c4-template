Use `cloud.backend._`.

Minimal snippet:

```likec4
view backend of cloud.backend {
  include cloud.backend
  include cloud.backend._
}
```

Why:
- `cloud.backend._` = only direct children of `cloud.backend` that are connected to already included elements in the view.
- `cloud.backend.*` = all direct children of `cloud.backend` (no relationship filter).
- `cloud.backend.**` = all descendants recursively (children, grandchildren, etc.).
# LikeC4 View Predicates: `*`, `_`, and `**`

## Answer

Use **`cloud.backend.*`**.

This predicate includes only the **direct children** of `cloud.backend` that have **at least one relationship** with elements already present in the view. It is the "relational wildcard" — it filters children by connectivity.

## Minimal view snippet

```likec4
view backendDetail of cloud.backend {
  include cloud.backend
  include cloud.backend.*
}
```

After `cloud.backend` is included, `cloud.backend.*` expands to whichever direct children are connected to it (or to any other element already in the view).

---

## What the other two would have selected

| Predicate | Scope | Relationship filter |
|---|---|---|
| `cloud.backend.*` | Direct children only | **Yes** — only children with ≥1 relationship to already-included elements |
| `cloud.backend._` | Direct children only | **No** — includes *all* direct children regardless of relationships |
| `cloud.backend.**` | All descendants recursively | **No** — includes *all* nested elements at every depth, with no relationship filter |

### `cloud.backend._`
Selects every immediate child of `cloud.backend` unconditionally. Use this when you want a complete flat list of direct children whether or not they are connected to anything in the current view.

### `cloud.backend.**`
Selects the full subtree — direct children, grandchildren, and deeper — with no relationship filter. Use this when you want to expand all nested elements of `cloud.backend` completely, regardless of their connectivity.
