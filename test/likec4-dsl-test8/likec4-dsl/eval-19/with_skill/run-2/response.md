- Base include set: in `view backend of cloud.backend { include * }`, `*` means `cloud.backend` itself plus its **direct children** only as the starting set, and direct relationships among those visible scoped elements; it does not recurse into grandchildren.
- Additional visibility: from that scoped base, relationship predicates can still bring in external neighboring elements and the matching incoming/outgoing relationships needed to render edges around `cloud.backend`, even though those neighbors are not part of the base subtree.

```likec4
views {
  view backend of cloud.backend {
    include *
    include -> cloud.backend ->
  }
}
```