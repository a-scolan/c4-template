# Detail view extending `backend-overview`

## DSL

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```

## Explanation

### 1. `extends backend-overview`
The `extends` keyword makes `backend-detail` inherit everything already defined in `backend-overview` — its scope element (`cloud.backend`) and all its `include`/`exclude` rules. You start with a copy of the parent view and can add or override rules on top.

### 2. Scope inheritance and `include api`
Because `backend-detail` extends `backend-overview`, it inherits the **scope** of that view, which is `cloud.backend`. Inside a scoped view (`view X of some.element`), unqualified names are resolved relative to that scope element. So `api` resolves to `cloud.backend.api` automatically — you don't need to write the full FQN. This is scope inheritance: child views keep the parent's element scope for name resolution.

### 3. `include -> cloud.backend`
The predicate `-> cloud.backend` is a **relationship predicate** that matches all relationships whose **target** is `cloud.backend`. Writing `include -> cloud.backend` adds every element that has an outgoing relationship pointing to `cloud.backend`, along with those relationship edges, into the view. This surfaces all callers/producers of the backend from the rest of the model without listing them individually.
