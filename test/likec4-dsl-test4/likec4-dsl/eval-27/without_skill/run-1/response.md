B — `include *` in a scoped view (`view backend of cloud.backend`) means `cloud.backend` plus its direct children as the base include set, because the implicit scope already anchors the view to `cloud.backend` and the wildcard expands one level (the element itself and its immediate children), not the full recursive subtree.

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend
}
```

`include -> cloud.backend` adds all elements that have a direct outgoing relationship pointing to `cloud.backend`, making their incoming connections visible in the view.
