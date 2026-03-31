```likec4
views {
  view detail extends backend-overview {
    include api
    include -> cloud.backend
  }
}
```

`detail` inherits the scope of `backend-overview` (which is `of cloud.backend`).
So `include api` resolves to `cloud.backend.api` without repeating the full FQN. The relationship predicate `include -> cloud.backend` adds all incoming relationships whose target is `cloud.backend` from elements outside (or elsewhere in) the accumulated/model context.