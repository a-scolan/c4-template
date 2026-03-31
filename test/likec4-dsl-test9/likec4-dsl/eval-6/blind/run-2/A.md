Use `cloud.backend._`.

```likec4
view backend_related_children of cloud.backend {
  include cloud.frontend
  include cloud.backend._
}
```

`cloud.backend._` includes only the **direct children** of `cloud.backend` that have at least one relationship with elements that are **already included in the view**.

What the other two would select instead:

- `cloud.backend.*` — **all direct children** of `cloud.backend`, whether they relate to the current view or not.
- `cloud.backend.**` — **all descendants recursively** under `cloud.backend` (children, grandchildren, etc.), again without filtering by whether they relate to the current view.
