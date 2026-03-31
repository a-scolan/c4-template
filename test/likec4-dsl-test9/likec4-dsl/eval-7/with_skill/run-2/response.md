```likec4
views {
  view backend-overview of cloud.backend {
    include *
  }

  view backend-detail extends backend-overview {
    include api
    include -> cloud.backend
  }
}
```

Scope inheritance here means `backend-detail` keeps the same scope as `backend-overview`, so it is still effectively a view `of cloud.backend`. Because of that inherited scope, the short reference `api` is resolved relative to `cloud.backend`, so it means `cloud.backend.api` rather than requiring the full FQN.

The relationship predicate `include -> cloud.backend` adds all incoming relationships whose target is `cloud.backend`. LikeC4 will also bring in the external source elements needed to render those inbound edges in the extended view.