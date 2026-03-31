```likec4
view detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```

`detail` inherits the scope of `backend-overview`, which is `cloud.backend`. That is why `include api` is enough here: inside the extended view, `api` is resolved relative to the inherited scope, so it means `cloud.backend.api`.

The relationship predicate `* -> cloud.backend` matches every relationship whose target is `cloud.backend`, so it pulls in all incoming relationships from elsewhere in the model.