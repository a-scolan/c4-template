B — In `view backend of cloud.backend`, `include *` means the base include set is `cloud.backend` plus its direct children.

```likec4
views {
  view backend of cloud.backend {
    include *
    include -> cloud.backend
  }
}
```