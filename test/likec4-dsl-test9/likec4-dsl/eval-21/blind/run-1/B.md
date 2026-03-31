Valid as written.

`extends` inherits the parent view definition, including the original `of cloud.backend` scope, so the child view does not need to redeclare `of cloud.backend`. In that scoped child view, `include api` resolves within the inherited scope, and the smallest way to also bring in incoming relationships to `cloud.backend` is to add `include -> cloud.backend`.

```likec4
view backend-overview of cloud.backend {
  include *
}

view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```