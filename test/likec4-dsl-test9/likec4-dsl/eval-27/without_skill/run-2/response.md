B — `include *` in a scoped view uses the current scope element (`cloud.backend`) plus its direct children as the base include set, not the full recursive subtree or the whole model.

```likec4
view backend of cloud.backend {
  include *
  include incoming cloud.backend
}
```