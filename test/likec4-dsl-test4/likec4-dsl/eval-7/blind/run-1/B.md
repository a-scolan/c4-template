# Detail View Extending `backend-overview`

## DSL

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```

## Explanation

### 1. `extends backend-overview`
The `extends` keyword makes this view inherit everything already declared in `backend-overview` — its scope element (`cloud.backend`) and all its `include` / `exclude` / `style` rules. You don't need to repeat `include *`.

### 2. Scope inheritance and `include api`
Because the base view is `of cloud.backend`, the **scope** of this view is `cloud.backend`. Inside any view with an explicit scope, unqualified names are resolved relative to that scope. So `api` is resolved as `cloud.backend.api` automatically — no need to write the full FQN.

### 3. `include -> cloud.backend`
The relationship predicate `-> cloud.backend` matches all **incoming** relationships whose target is `cloud.backend`, regardless of where the source lives in the model. This brings in every element that has an outgoing relationship pointing to `cloud.backend`, together with the relationship arrow itself.

> **Note:** if you only want the relationship arrows without pulling in the source elements automatically, some LikeC4 versions support `include cloud.backend with { incoming }` style predicates — but the `-> target` predicate form shown above is the standard portable syntax.
