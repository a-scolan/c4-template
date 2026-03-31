Use `cloud.backend._`.

```likec4
views {
  view backend-related-children of cloud.backend {
    include cloud.backend._
  }
}
```

Why:
- `cloud.backend._` = the **direct children** of `cloud.backend` that have at least one relationship with the elements already accumulated in the view (in a scoped view, that effectively means the scope/context already in play, not every child).
- `cloud.backend.*` = **all direct children** of `cloud.backend`, whether they are connected or not.
- `cloud.backend.**` = **recursive descendants** of `cloud.backend` (children, grandchildren, deeper) that have relationships with the accumulated result — so it can pull in deeper nested elements, not just immediate children.
