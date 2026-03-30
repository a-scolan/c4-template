Valid as written.

`backend-detail` inherits the scope from `backend-overview` because `extends` carries over the base view context (`of cloud.backend`), so `include api` resolves within that inherited scope and does not need `of cloud.backend` again.

```likec4
view backend-overview of cloud.backend {
  include *
}

view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```