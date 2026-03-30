B

In a scoped view, `include *` means the scoped element plus its direct children as the base include set, not the full recursive subtree and not the whole model.

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend
}
```