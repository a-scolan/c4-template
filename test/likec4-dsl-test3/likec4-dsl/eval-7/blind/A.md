```likec4
detail view backend-detail extends backend-overview {
  include api
  include relationship where target == cloud.backend and source != cloud.backend
}
```

`backend-detail` extends `backend-overview`, so it inherits the same scope (`of cloud.backend`) from the base view. That is why `include api` resolves to `cloud.backend.api` automatically (no full FQN needed). In other words, scope inheritance means unqualified element names inside the extending view are evaluated relative to the inherited scoped element.