- Base include set: in `view backend of cloud.backend { include * }`, `*` includes `cloud.backend` itself plus its `direct children` as the starting set.
- Neighboring/derived visibility: that does **not** mean the whole model, but relationships touching that scoped set can still make connected external neighbors and their matching incoming/outgoing relationships visible when you add relationship predicates around `cloud.backend`.

```likec4
view backend of cloud.backend {
  include *
  include -> cloud.backend ->
}
```