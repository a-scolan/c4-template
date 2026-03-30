```likec4
view backend-overview of cloud.backend {
  include *
}

view backend-detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```

Here, scope inheritance means `backend-detail` keeps the same base scope (`of cloud.backend`) from `backend-overview`. So `include api` is resolved relative to that scope as `cloud.backend.api`, without writing the full FQN.
# LikeC4 Detail View with Scope Inheritance

## DSL

```likec4
view detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```

## Explanation

### 1. Extending `backend-overview`

`extends backend-overview` inherits all includes and the **scope element** of the parent view. The parent is declared `of cloud.backend`, so `cloud.backend` becomes the implicit scope for identifier resolution in any view that extends it.

### 2. Scope inheritance — what it means here

Because `backend-overview` is scoped to `cloud.backend`, that element is the resolution root inside any extending view. When the DSL parser sees `include api`, it looks up `api` relative to `cloud.backend` and resolves it to `cloud.backend.api`. You never need to write the full qualified name. This is **scope inheritance**: the extending view borrows the parent's `of <element>` context as its own default namespace.

### 3. Incoming relationship predicate

```likec4
include * -> cloud.backend
```

This is a **relationship predicate**. The `*` on the left side means "any element in the model", and `-> cloud.backend` constrains the direction to *incoming* relationships targeting `cloud.backend`. The predicate causes the view to pull in every element that has a direct relationship pointing to `cloud.backend`, together with those relationship edges — regardless of where those elements sit in the model hierarchy.

## Complete picture

| Statement | What it does |
|---|---|
| `extends backend-overview` | Inherits all included elements from the parent view and its `of cloud.backend` scope |
| `include api` | Adds `cloud.backend.api` (resolved via scope inheritance) |
| `include * -> cloud.backend` | Adds every element that sends a relationship to `cloud.backend`, plus those edges |
