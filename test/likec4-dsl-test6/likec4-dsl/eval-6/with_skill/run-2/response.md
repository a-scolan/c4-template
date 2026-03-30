Use `cloud.backend._`.

```likec4
views {
  view backend-related of cloud.backend {
    include -> cloud.backend ->
    include cloud.backend._
  }
}
```

- `cloud.backend._` selects only the direct children of `cloud.backend` that have relationships with the elements already accumulated in the view.
- `cloud.backend.*` would select all direct children of `cloud.backend`, whether they are connected or not.
- `cloud.backend.**` would select recursive descendants of `cloud.backend` that have relationships with the accumulated result, not just direct children.