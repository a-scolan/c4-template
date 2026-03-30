Valid as written.

A `view … extends …` inherits the parent view's full definition, including its `of` scope clause. Because `backend-overview` is scoped `of cloud.backend`, the child view `backend-detail` automatically operates in the same `cloud.backend` scope — meaning identifiers like `api` are resolved as `cloud.backend.api` without needing to re-declare `of cloud.backend`. Repeating `of cloud.backend` in the child is therefore unnecessary and would be redundant.

Smallest final snippet (inherits scope, adds `api`, and pulls in incoming relationships to `cloud.backend`):

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```

- `include api` resolves to `cloud.backend.api` via inherited scope.
- `include -> cloud.backend` is a relationship predicate that selects all relationships from the model that point **to** `cloud.backend`, and pulls their source elements into the view.
