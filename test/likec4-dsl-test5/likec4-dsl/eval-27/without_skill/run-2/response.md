B

`include *` in `view backend of cloud.backend` uses the scoped base set (`cloud.backend` and its direct children), not the whole model and not an automatic recursive subtree.

```c4
view backend of cloud.backend {
  include *
  include <- cloud.backend
}
```B

In a scoped view `view X of element`, `include *` expands to the scoped element itself plus its **direct children** as the base include set — it does not recurse into grandchildren (that would require explicit deeper includes or `include **` patterns).

## Minimal snippet

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend
}
```

`include -> cloud.backend` adds any element that has an outgoing relationship pointing **to** `cloud.backend`, surfacing all direct incomers alongside the existing direct-children base set.
