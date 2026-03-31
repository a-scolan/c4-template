cloud.backend._

```likec4
views {
  view backend of cloud.backend {
    include cloud.backend.api
    include cloud.backend._
  }
}
```

- `cloud.backend._` selects only the **direct children** of `cloud.backend` that have at least one relationship with elements already accumulated in the view.
- `cloud.backend.*` would select **all direct children** of `cloud.backend`, connected or not.
- `cloud.backend.**` would select **recursive descendants** of `cloud.backend` (children, grandchildren, etc.) that have relationships with the accumulated view, not just direct children.
