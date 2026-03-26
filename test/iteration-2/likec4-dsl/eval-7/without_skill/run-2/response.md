```likec4
view backend-overview of cloud.backend {
  include *
}

view detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```

Scope inheritance means `detail` keeps `of cloud.backend` from `backend-overview`, so `api` resolves as `cloud.backend.api` without repeating the full FQN.