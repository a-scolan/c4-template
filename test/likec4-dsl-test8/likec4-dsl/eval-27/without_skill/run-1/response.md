B — In a scoped view, `include *` uses the scoped element as the base include set, so it includes `cloud.backend` plus its direct children rather than the whole recursive subtree or the whole model.

```likec4
view backend of cloud.backend {
  include *
  include * -> cloud.backend
}
```
