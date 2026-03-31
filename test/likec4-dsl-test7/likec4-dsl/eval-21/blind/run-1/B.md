Valid as written.

`extends backend-overview` inherits the parent view scope (`of cloud.backend`), so the child view does not need to redeclare it. You only redeclare `of ...` when defining a fresh scoped view, not when extending one. To also include incoming relationships to `cloud.backend`, add a single relationship include targeting that element.

```likec4
view backend-detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```