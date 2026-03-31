B — in a scoped view, `include *` uses the scoped element `cloud.backend` plus its direct children as the base include set, rather than the whole recursive subtree or the whole model.

```likec4
view backend of cloud.backend {
  include *
  include * -> cloud.backend
}
```