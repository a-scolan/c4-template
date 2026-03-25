```likec4
views {
  view backend-overview of cloud.backend {
    include *
  }

  view detail extends backend-overview {
    include api
    include * -> cloud.backend
  }
}
```

`detail` inherits the parent view’s scope (`of cloud.backend`). That means unqualified references are resolved relative to `cloud.backend`, so `include api` is interpreted as `include cloud.backend.api`.

The relationship predicate `* -> cloud.backend` adds incoming relationships targeting `cloud.backend` (and includes matching source elements as needed).