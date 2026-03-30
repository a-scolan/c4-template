Valid as written.

When a view extends another view, it inherits the parent view scope, so `backend-detail` remains scoped to `cloud.backend` and does not need `of cloud.backend` again. Minimal snippet with incoming relationships to `cloud.backend`:

```likec4
view backend-detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```