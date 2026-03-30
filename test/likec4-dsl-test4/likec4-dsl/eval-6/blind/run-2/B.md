## Answer

Use **`cloud.backend._`**.

### Minimal view snippet

```likec4
view backend-detail of cloud.backend {
  include *
  include cloud.backend._
}
```

The `include *` first populates the accumulated result with `cloud.backend` and its direct children plus their relationships (as defined by the wildcard-in-scoped-view rule). Then `cloud.backend._` refines further to show only the children that actually connect to something already in the view.

In practice you often write just:

```likec4
view backend-detail of cloud.backend {
  include cloud.backend._
}
```

where the accumulated result before that line already contains the scoped element itself (from the view scope), so `_` filters children by their relationship to it.

---

### What the other two would have selected

| Predicate | Meaning | What it selects here |
|---|---|---|
| `cloud.backend.*` | All **direct children**, unconditionally | Every direct child of `cloud.backend`, whether it has any relationship or not — isolated children would appear as floating nodes |
| `cloud.backend._` | Direct children **that have at least one relationship** with the accumulated result | Only connected direct children — exactly what you want |
| `cloud.backend.**` | **All recursive descendants** that have relationships with accumulated result | Not just direct children: grandchildren, great-grandchildren, etc. are also included if they have a relationship with accumulated result |

### Summary

- `.*` → all direct children, no relationship filter  
- `._` → direct children **only if connected** (use this)  
- `.**` → all nested descendants (recursive), relationship-filtered
