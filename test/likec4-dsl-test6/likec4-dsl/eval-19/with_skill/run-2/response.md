- Base include set: in a scoped view, `include *` includes the scoped element `cloud.backend`, its direct children, and the relationships among that included set.
- Neighboring/derived visibility: additional external neighbor elements and their connecting relationships can still appear when later predicates add incoming or outgoing relationships around `cloud.backend`.

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend ->
}
```