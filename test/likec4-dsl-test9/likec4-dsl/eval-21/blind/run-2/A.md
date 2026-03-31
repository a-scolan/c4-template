Valid as written.

`extends backend-overview` inherits the parent view definition, including the original `of cloud.backend` scope, so the child view stays scoped to `cloud.backend` without redeclaring it. To also show callers into that scoped backend, add an inbound relationship predicate such as `include -> cloud.backend`; that expands visible incoming edges while keeping the inherited scope unchanged.

```likec4
view backend-overview of cloud.backend {
  include *
}

view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```