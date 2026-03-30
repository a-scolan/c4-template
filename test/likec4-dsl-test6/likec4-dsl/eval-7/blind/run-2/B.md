```likec4
view backend-overview of cloud.backend {
  include *
}

detail view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```

Scope inheritance means the `detail` view keeps the scope of `backend-overview`, so inside the extended view `api` is resolved relative to `cloud.backend`. That is why `include api` is enough and you do not need to write the full FQN `cloud.backend.api`. The relationship predicate `include -> cloud.backend` adds all incoming relationships to `cloud.backend` from elsewhere in the model.