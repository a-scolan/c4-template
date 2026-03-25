Use `cloud.backend._`.

```likec4
views {
  view backend-connected-children of cloud.backend {
    include cloud.backend
    include cloud.backend._
  }
}
```

Why this one:
- `cloud.backend._` = **direct children only** of `cloud.backend` that have at least one relationship with the **already accumulated** view result.

What the others would select:
- `cloud.backend.*` = **all direct children** (1 level), regardless of whether they are connected to already included elements.
- `cloud.backend.**` = **recursive descendants** (children, grandchildren, etc.) that have relationships with already included elements (not limited to direct children).