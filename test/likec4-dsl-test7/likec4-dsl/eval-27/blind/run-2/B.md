B — In a scoped view, `include *` expands to the scoped element (`cloud.backend`) and its direct children as the base include set, not the full recursive subtree or whole model.

```likec4
view backend of cloud.backend {
  include *
  include * -> cloud.backend
}
```