B — in a scoped `view ... of cloud.backend`, `include *` expands to the base include set of the scoped element plus its direct children, not the whole model and not the full recursive subtree by default.

```likec4
view backend of cloud.backend {
  include *
  include <- cloud.backend
}
```
B

In a scoped view, `include *` resolves relative to the view's scope element, so it includes `cloud.backend` itself plus its direct children as the base include set — not the full recursive subtree and not the whole model.

**Minimal snippet keeping `include *` and adding incoming relationships around `cloud.backend`:**

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend
}
```

`include -> cloud.backend` adds all elements that have a direct outgoing relationship pointing to `cloud.backend`, making their connections visible without expanding the rest of the model.
