```likec4
views {
  view backend-overview of cloud.backend {
    include *
  }

  view detail extends backend-overview {
    include api
    include -> cloud.backend
  }
}
```

`detail` inherits from `backend-overview`, including its scope (`of cloud.backend`). That scope inheritance means unqualified references inside `detail` are resolved relative to `cloud.backend`, so `include api` is equivalent to `include cloud.backend.api`.

The relationship predicate `include -> cloud.backend` adds incoming relationships to `cloud.backend` (and pulls in the source neighbors from outside the scoped subtree as needed).