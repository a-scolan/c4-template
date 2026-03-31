```likec4
views {
  view detail extends backend-overview {
    include api
    include -> cloud.backend
  }
}
```

Scope inheritance here means `detail` inherits the same scope as `backend-overview`, which is `of cloud.backend`. Because of that, `api` is resolved relative to `cloud.backend`, so `include api` means `include cloud.backend.api` without repeating the full FQN.

It also inherits the parent view’s rules, so the original `include *` still applies; this new view just adds to that inherited result. The relationship predicate `include -> cloud.backend` adds incoming relationships to `cloud.backend` and pulls in the external source elements for those relationships.