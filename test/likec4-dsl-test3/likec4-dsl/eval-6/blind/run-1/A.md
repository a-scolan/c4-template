Use `cloud.backend._`.

A minimal snippet is:

```likec4
view of cloud.backend {
  include cloud.backend._
}
```

Why:
- `cloud.backend._` = only **direct children** of `cloud.backend` that have at least one relationship with elements already included in the view.
- `cloud.backend.*` = **all direct children** of `cloud.backend` (no relationship-based filtering).
- `cloud.backend.**` = **all descendants recursively** (children, grandchildren, etc.), also not limited to only related direct children.