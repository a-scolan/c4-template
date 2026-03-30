# Answer

Use `cloud.backend._` to include only direct children of `cloud.backend` **that have at least one relationship** with elements already in the view.

## Minimal view snippet

```likec4
view backendView of cloud.backend {
  include *
  include cloud.backend._
}
```

The `include *` line brings in `cloud.backend` itself (and the surrounding context for a scoped view). Then `cloud.backend._` adds only those direct children that are connected (have a relationship) to something already included.

---

## What the other two would select

| Predicate | Meaning |
|---|---|
| `cloud.backend.*` | All **direct children** of `cloud.backend`, **regardless of whether they have any relationship** with the already-included elements. Every immediate child is added unconditionally. |
| `cloud.backend.**` | All **descendants** of `cloud.backend` at **any depth** (children, grandchildren, …), again unconditionally — no relationship filter. |
| `cloud.backend._` | Direct children only, **filtered**: only those that share at least one relationship with an element already present in the view. |

So the key distinction is:
- `*` → direct children, no filter
- `**` → all descendants, no filter  
- `_` → direct children, relationship-filtered (connected nodes only)
