- `include *` in `view backend of cloud.backend { ... }` starts from `cloud.backend` plus its **direct children** only, and it also includes direct relationships defined at that same scope; it is neither the whole model nor a recursive subtree.
- From that scoped base, outside neighbors can still become visible when relationship predicates are added, because LikeC4 brings in the external endpoints needed to render those incoming/outgoing edges; direct scoped relationships are visible, but grandchildren are still not unless you include them separately.

```likec4
views {
  view backend of cloud.backend {
    include *
    include -> cloud.backend ->
  }
}
```