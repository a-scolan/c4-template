Use `cloud.backend._`.

```likec4
views {
  view backend-related of cloud.backend {
    include cloud.backend
    include cloud.backend._
  }
}
```

- `cloud.backend._` selects only **direct children** of `cloud.backend` that have at least one relationship with the already included set.
- `cloud.backend.*` would select **all direct children** (even without such relationships).
- `cloud.backend.**` would select **recursive descendants** (children, grandchildren, etc.) that have relationships with the included set.