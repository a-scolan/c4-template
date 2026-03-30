B

In a scoped view, the wildcard `*` is explicitly defined as selecting the scoped element (`cloud.backend`) plus its **direct children** as the base include set — not the recursive subtree (that would be `**`), and not the whole model (which is what an unscoped `include *` does).

```likec4
view backend of cloud.backend {
  include *
  include * -> cloud.backend
}
```

`include * -> cloud.backend` adds all relationships from any model element to `cloud.backend`, pulling in the external source elements along with those incoming connections.
