- Base include set: in `view backend of cloud.backend { include * }`, `*` includes the scoped element `cloud.backend` plus its **direct children** only; it does not recursively include grandchildren or the whole model.
- Neighboring/derived visibility: external neighbors and their edges can still appear when you add relationship predicates around the scope, so inbound and outbound relationships for `cloud.backend` become visible even though they are not part of the base `include *` set.

```likec4
views {
  view backend of cloud.backend {
    include *
    include -> cloud.backend
    include cloud.backend ->
  }
}
```