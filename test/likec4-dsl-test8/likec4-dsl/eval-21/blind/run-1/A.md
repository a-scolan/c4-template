Valid as written.

`extends backend-overview` inherits the base view’s scope, so `backend-detail` is still scoped `of cloud.backend` and does not need that clause again. To also show incoming relationships to `cloud.backend`, add a relationship include that targets it.

```likec4
view backend-detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```