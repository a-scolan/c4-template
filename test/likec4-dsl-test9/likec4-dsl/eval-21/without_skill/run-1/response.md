Valid as written.

A child view that `extends backend-overview` inherits the parent view’s subject scope, so you do **not** need to repeat `of cloud.backend`. To also show incoming relationships to `cloud.backend`, add an incoming-neighborhood inclusion to the child view while keeping the override as small as possible:

```likec4
view backend-detail extends backend-overview {
  include api
  include <- cloud.backend
}
```