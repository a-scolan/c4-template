## Answer

Use **`cloud.backend._`**.

### Minimal view snippet

```likec4
view backend-detail of cloud.backend {
  include *
  include cloud.backend._
}
```

`include *` (wildcard in a scoped view) first brings in `cloud.backend`, its direct children, and their mutual relationships. `cloud.backend._` then adds only the direct children that already have at least one relationship with the elements accumulated so far — so children with no connections are silently omitted.

---

### What the other two would have selected instead

| Predicate | What it selects |
|-----------|----------------|
| `cloud.backend.*` | **All** direct children of `cloud.backend`, unconditionally — including isolated children with zero relationships to the rest of the view. |
| `cloud.backend.**` | All **recursive descendants** of `cloud.backend` (children, grandchildren, …) that have at least one relationship with the accumulated result — goes deeper than one level, not restricted to direct children. |

In short:
- `*` = all direct children, no relationship filter
- `_` = direct children **only if connected** (use this for the stated goal)
- `**` = all descendants recursively that are connected (too deep)
