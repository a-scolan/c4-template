Use `cloud.backend._`.

Minimal snippet:

```likec4
view backend_filtered of cloud.backend {
  include cloud.frontend
  include cloud.backend._
}
```

Why this one:
- `cloud.backend._` = only **direct children** of `cloud.backend` that have at least one relationship with elements already included in the view.

What the others would select:
- `cloud.backend.*` = **all direct children** of `cloud.backend` (no relationship filter).
- `cloud.backend.**` = **all descendants recursively** (children, grandchildren, etc.; no relationship filter).