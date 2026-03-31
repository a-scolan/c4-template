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

`detail` inherits the scope of `backend-overview`, so it is still evaluated in the `cloud.backend` context even though it does not repeat `of cloud.backend`. In this case, scope inheritance means the child view can resolve `include api` relative to that inherited scope, so `api` is interpreted as `cloud.backend.api`, and `include -> cloud.backend` adds all inbound relationships targeting `cloud.backend` from elsewhere in the model.