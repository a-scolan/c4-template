```likec4
views {
  view detail extends backend-overview {
    include api
    include -> cloud.backend
  }
}
```

`detail` inherits the scope of `backend-overview`, so it is still scoped `of cloud.backend` even though that clause is not repeated. In that inherited scope, the unqualified reference `api` resolves relative to `cloud.backend`, so `include api` means `include cloud.backend.api`. The relationship predicate `include -> cloud.backend` adds all incoming relationships that target `cloud.backend`, bringing in the external callers needed to render those inbound edges.