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

Scope inheritance means `detail` keeps the same scope as `backend-overview` (`of cloud.backend`), so `include api` resolves to `cloud.backend.api` without repeating the full FQN.