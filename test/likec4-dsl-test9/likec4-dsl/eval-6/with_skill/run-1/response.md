`cloud.backend._`

```likec4
views {
  view backend-neighbors of cloud.backend {
    include -> cloud.backend
    include cloud.backend._
  }
}
```

Use `cloud.backend._`.

In this dotted form, `_` means: include only the **direct children** of `cloud.backend` that have at least one relationship with the elements that are **already included** in the view.

What the other two would do instead:

- `cloud.backend.*` — includes **all direct children** of `cloud.backend`, whether they are connected to the current view contents or not.
- `cloud.backend.**` — includes only **connected descendants recursively**, so it can bring in grandchildren and deeper elements too, not just the direct children.
