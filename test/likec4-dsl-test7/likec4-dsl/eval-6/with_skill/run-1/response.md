Use `cloud.backend._`.

```likec4
views {
  view backend of cloud.backend {
    include cloud.backend._
  }
}
```

What the others would select:
- `cloud.backend.*` → **all direct children** of `cloud.backend` (relationship not required).
- `cloud.backend._` → only direct children that have at least one relationship with the accumulated included set.
- `cloud.backend.**` → recursive descendants (children, grandchildren, etc.) that have such relationships.