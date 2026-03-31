Valid as written.

An `extends` view inherits the base view’s scope, so `backend-detail` is still a view of `cloud.backend` and does not need `of cloud.backend` repeated. To also show relationships coming into `cloud.backend`, add an incoming relationship include such as `* -> cloud.backend`.

```likec4
view backend-overview of cloud.backend {
  include *
}

view backend-detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```