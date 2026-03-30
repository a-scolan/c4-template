- Base include set: in `view backend of cloud.backend`, `include *` includes `cloud.backend` and its **direct children** (and, by scoped expansion, their nested descendants inside that subtree).
- Additional visibility: because the subtree is included in a scoped view, neighbors connected by incoming/outgoing relationships and implied/derived edges around the scoped element can still be brought into view when those relationship includes are declared.

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend
  include cloud.backend ->
}
```