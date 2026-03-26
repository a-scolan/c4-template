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

Scope inheritance means `detail` keeps the parent view scope (`of cloud.backend`), so `api` resolves to `cloud.backend.api` without writing the full FQN.