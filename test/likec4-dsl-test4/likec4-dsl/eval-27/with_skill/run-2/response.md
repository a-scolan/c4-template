B — in a scoped view `of cloud.backend`, `include *` selects `cloud.backend` plus its **direct children** as the base include set (along with all relationships between them), not the full recursive subtree and not the whole model.

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend
}
```
