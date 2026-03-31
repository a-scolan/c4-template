Valid as written.

A view that `extends` a scoped parent inherits that parent view’s scope, so `backend-detail` stays scoped to `cloud.backend` and does not need `of cloud.backend` again. The child view just adds rules on top of `backend-overview`, so this is the minimal update to keep the inherited scope and add inbound relationships to `cloud.backend`.

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```