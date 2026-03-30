Valid as written.

The child view inherits the subject scope from `backend-overview`, so `extends backend-overview` does not need `of cloud.backend` again; you only restate the scope if you are defining a new independent view instead of extending the existing scoped one.

```likec4
view backend-overview of cloud.backend {
  include *
}

view backend-detail extends backend-overview {
  include api
  include <- cloud.backend
}
```