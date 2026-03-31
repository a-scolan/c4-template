B — in a scoped view, `include *` means `cloud.backend` plus its direct children as the base include set, not the recursive subtree or the whole model.

```likec4
views {
  view backend of cloud.backend {
    include *
    include -> cloud.backend
  }
}
```