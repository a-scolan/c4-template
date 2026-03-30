Use `cloud.backend._`.

```likec4
view of cloud.backend {
  include cloud.backend
  include cloud.backend._ where hasRelationshipWithIncluded()
}
```

- `cloud.backend._` = only direct children of `cloud.backend` (one level).
- `cloud.backend.*` = `cloud.backend` plus all of its direct children.
- `cloud.backend.**` = `cloud.backend` plus all descendants at any depth (children, grandchildren, etc.).
# LikeC4 View Predicates: `*`, `_`, and `**`

## Answer

Use **`cloud.backend._`** to include only direct children of `cloud.backend` that have at least one relationship with elements already present in the view.

## Minimal view snippet

```likec4
view backendView of cloud.backend {
  include cloud.backend
  include cloud.backend._
}
```

`cloud.backend` is first included explicitly (the scope element), then `cloud.backend._` adds only its direct children that are connected (have at least one relationship) to elements already in the view — i.e., to `cloud.backend` itself or to each other as they are progressively added.

---

## What the other two would have selected

| Predicate | What it selects |
|---|---|
| `cloud.backend.*` | **All** direct children of `cloud.backend`, regardless of whether they have any relationships with other elements in the view. Useful for a complete breakdown of every immediate child. |
| `cloud.backend.**` | **All descendants** of `cloud.backend` recursively (children, grandchildren, …), again regardless of relationships. Useful when you want to expand the entire subtree. |
| `cloud.backend._` ✓ | Only the direct children of `cloud.backend` that share **at least one relationship** with an element already included in the view. Keeps the diagram focused on connected parts. |

---

## Summary

- `_` → connected direct children (relationship-filtered)
- `*` → all direct children (no filter)
- `**` → all descendants recursively (no filter)
