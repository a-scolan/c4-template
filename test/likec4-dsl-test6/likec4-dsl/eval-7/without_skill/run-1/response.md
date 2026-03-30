```likec4
view backend-overview of cloud.backend {
  include *
}

view detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```

Scope inheritance here means `detail` keeps the same scope as `backend-overview` (`of cloud.backend`), so `include api` is resolved as `cloud.backend.api` automatically without writing the full FQN.