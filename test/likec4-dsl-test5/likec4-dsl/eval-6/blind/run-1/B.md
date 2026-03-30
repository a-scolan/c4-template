Use `cloud.backend._`.

```likec4
views {
  view backend-related of cloud.backend {
    include -> cloud.backend ->
    include cloud.backend._
  }
}
```

- `cloud.backend._` selects only direct children of `cloud.backend` that have relationships with the already accumulated result.
- `cloud.backend.*` would select all direct children, including unconnected ones.
- `cloud.backend.**` would select recursive descendants (children, grandchildren, etc.) that have relationships with the accumulated result.