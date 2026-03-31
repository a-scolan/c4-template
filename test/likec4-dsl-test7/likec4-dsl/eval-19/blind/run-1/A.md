- The base include set is **the scoped element `cloud.backend` plus its direct children**; `*` in a scoped view is not the whole model, and it is not the full recursive subtree.
- Neighboring elements outside that subtree can still become visible when relationships touching `cloud.backend` (or already included elements) are included, because relationship predicates bring in the matched relationships **and their endpoint elements**.

```likec4
views {
  view backend of cloud.backend {
    include *
    include -> cloud.backend ->
  }
}
```