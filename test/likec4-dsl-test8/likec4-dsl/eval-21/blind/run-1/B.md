Valid as written.

`backend-detail` inherits the scope of `backend-overview`, so you do not need to repeat `of cloud.backend`. In an extended scoped view, additional predicates like `include api` are evaluated within the inherited scope, and `extends` just adds rules on top of the parent view.

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```