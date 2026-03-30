B
In a scoped view `of cloud.backend`, `include *` initializes the view with `cloud.backend` and its direct children, not the full recursive subtree or whole model.

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend
}
```