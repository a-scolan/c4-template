Use `cloud.backend._`.

```likec4
view backend-connected-children of cloud.backend {
  include -> cloud.backend ->
  include cloud.backend._
}
```

`cloud.backend.*` would select all direct children of `cloud.backend`, whether they are connected to the accumulated result or not. `cloud.backend.**` would select recursive descendants of `cloud.backend` that are connected to the accumulated result, not just direct children.