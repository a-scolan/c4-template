`cloud.backend._`

```likec4
views {
  view backend-related of cloud.backend {
    include -> cloud.backend
    include cloud.backend._
  }
}
```

- `cloud.backend._` selects only the **direct children** of `cloud.backend` that have at least one relationship with elements already accumulated in the view.
- `cloud.backend.*` would select **all direct children** of `cloud.backend`, whether they are connected or not.
- `cloud.backend.**` would select **recursive descendants** of `cloud.backend` that are connected to the already included elements, so it can pull in grandchildren and deeper descendants too.

In the snippet above, `include -> cloud.backend` seeds the view with already-included neighbors, and `include cloud.backend._` adds only the direct child elements of `cloud.backend` that are actually connected to that current result set.
