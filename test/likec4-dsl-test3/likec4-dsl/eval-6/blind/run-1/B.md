Use `cloud.backend._`.

```likec4
views {
  view backend-related-children of cloud.backend {
    // assume previous include rules already added some context elements
    include cloud.backend._
  }
}
```

Why this one:
- `cloud.backend._` = **direct children only** of `cloud.backend` that have at least one relationship with the **already included** elements.

What the others would select:
- `cloud.backend.*` = **all direct children** (1 level), regardless of whether they relate to already included elements.
- `cloud.backend.**` = **all recursive descendants** (children, grandchildren, etc.) that relate to already included elements — broader depth than requested.