B — in a scoped view, `include *` means `cloud.backend` plus its direct children as the base include set, not recursive descendants and not the whole model.

```likec4
views {
  view backend of cloud.backend {
    include *
    include -> cloud.backend
  }
}
```