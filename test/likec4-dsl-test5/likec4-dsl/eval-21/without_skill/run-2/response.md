Valid as written.

The child view inherits the scope from `backend-overview` through `extends`, so it does not need to repeat `of cloud.backend`; you only add additional include rules in the extending view.

```likec4
view backend-detail extends backend-overview {
  include api
  include <- cloud.backend
}
```# Eval-21 Response

**Valid as written.**

When a view uses `extends`, it inherits the scope (`of <element>`) from the parent view. Because `backend-overview` is already scoped `of cloud.backend`, the child view `backend-detail extends backend-overview` automatically operates within that same scope — the identifier `api` is resolved relative to `cloud.backend` without redeclaring it. Repeating `of cloud.backend` would be redundant (and in most LikeC4 versions is not even allowed alongside `extends`).

## Smallest final snippet with incoming relationships

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```

`include -> cloud.backend` adds all elements that have an outgoing relationship pointing **to** `cloud.backend`, i.e. its incomers, along with those relationship edges.
