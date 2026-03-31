Valid as written.

When a view `extends` another view in LikeC4, it inherits the parent view context/scope, so you do not need to repeat `of cloud.backend` in the child definition. To also include incoming relationships to `cloud.backend`, add a single include rule for inbound edges.

```likec4
view backend-overview of cloud.backend {
  include *
}

view backend-detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```