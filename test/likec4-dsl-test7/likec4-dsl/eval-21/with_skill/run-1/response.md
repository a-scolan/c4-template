Valid as written.

`extends` inherits the parent view’s scope and accumulated rules, so `backend-detail` remains scoped to `cloud.backend` and `include api` is resolved inside that same scope; you do not need to repeat `of cloud.backend`. To add only incoming relationships to `cloud.backend`, append the canonical inbound predicate.

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```