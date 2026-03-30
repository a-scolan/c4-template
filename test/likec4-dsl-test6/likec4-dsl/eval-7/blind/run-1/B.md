```likec4
view detail extends backend-overview {
  include api
  include -> cloud.backend
}
```

Scope inheritance means `detail` keeps the `of cloud.backend` scope from `backend-overview`, so `api` is resolved as `cloud.backend.api` without needing the full FQN.