- The base set of `include *` in `view backend of cloud.backend { ... }` is `cloud.backend` itself plus its **direct children** (one level only), and the direct relationships already defined at that same scoped level; it does **not** recurse into grandchildren or the whole model.
- From that scoped base, additional external neighbors can still become visible when you include incoming/outgoing relationships touching `cloud.backend` (or visible scoped elements): the neighbor elements are pulled in only as needed to render those edges, so they are derived from relationship visibility rather than belonging to the base `*` set.

```likec4
views {
  view backend of cloud.backend {
    include *
    include -> cloud.backend ->
  }
}
```