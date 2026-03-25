view backend-detail extends backend-overview {
  include api
  include * -> cloud.backend
}

Scope inheritance here means `backend-detail` automatically keeps the same scope as `backend-overview`, which is `of cloud.backend`. Because of that, `include api` is resolved relative to `cloud.backend`, so it means the `api` element inside `cloud.backend` rather than requiring you to write the full path again. The relationship predicate `include * -> cloud.backend` adds every incoming relationship whose target is `cloud.backend`, pulling in external sources from elsewhere in the model as needed.
