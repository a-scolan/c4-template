B — In a scoped view, `include *` sets the base include set to `cloud.backend` plus its direct children only, not the recursive subtree and not the whole model.

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend
}
```