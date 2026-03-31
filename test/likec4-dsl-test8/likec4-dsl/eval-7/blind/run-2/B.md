```likec4
views {
  view detail extends backend-overview {
    include api
    include -> cloud.backend
  }
}
```

Scope inheritance means `detail` keeps the same scope as `backend-overview`, which is `cloud.backend`. So `include api` is resolved relative to that scope as `cloud.backend.api`, and you do not need to repeat the full FQN. The relationship predicate `include -> cloud.backend` adds all incoming relationships whose target is `cloud.backend`, which brings in callers from elsewhere in the model as needed to render those inbound edges.
