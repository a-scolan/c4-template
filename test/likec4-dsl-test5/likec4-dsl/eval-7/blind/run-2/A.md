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

Scope inheritance means `detail` inherits the parent view scope (`of cloud.backend`), so `include api` resolves to `cloud.backend.api` without repeating the full FQN.