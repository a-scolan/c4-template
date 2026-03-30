Valid as written.

A view that `extends` another view inherits the parent view’s definition, so you do not need to repeat `of cloud.backend`; the child can add rules on top of that inherited scoped view, which is why `include api` is valid here.

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```