Use `cloud.backend._`.

```likec4
view backend_filtered of cloud.backend {
  include cloud.frontend
  include cloud.backend._
}
```

Why:
- `cloud.backend._` = only **direct children** of `cloud.backend` that have at least one relationship with elements already included in the view.
- `cloud.backend.*` = **all direct children** of `cloud.backend` (relationship not required).
- `cloud.backend.**` = **all descendants recursively** (children, grandchildren, etc.), regardless of whether they relate to already included elements.