B

In a scoped view, `include *` starts from the scoped element and its direct children, not the full recursive subtree and not the whole model.

```likec4
view backend of cloud.backend {
  include *
  include <- cloud.backend
}
```