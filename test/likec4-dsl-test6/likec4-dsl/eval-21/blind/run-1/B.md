Valid as written.

A child view that `extends` a scoped parent inherits that parent's scope, so `backend-detail` does not need to repeat `of cloud.backend`; it can add rules on top of `backend-overview`, and `include api` stays scoped to that same backend context.

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```