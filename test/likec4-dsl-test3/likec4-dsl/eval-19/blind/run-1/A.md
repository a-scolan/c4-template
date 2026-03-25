In `view backend of cloud.backend { include * }`, `*` is **scoped** — it includes:
- `cloud.backend` itself,
- its **direct children**,
- and relationships involving those included elements.

It does **not** include the whole model.

```likec4
views {
  view backend of cloud.backend {
    include *
    include -> cloud.backend ->   // only incoming + outgoing around cloud.backend
  }
}
```