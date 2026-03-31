Valid as written.

`extends` inherits the parent view definition, including its scoped context, so `backend-detail` does not need `of cloud.backend` again. In this case `include api` is resolved within the inherited `cloud.backend` scope, and the smallest way to add inbound relationships to `cloud.backend` is `include -> cloud.backend`.

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```