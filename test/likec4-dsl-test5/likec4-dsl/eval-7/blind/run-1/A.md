```likec4
view backend-overview of cloud.backend {
  include *
}

view backend-detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```

`backend-detail` inherits the scope from `backend-overview` (`of cloud.backend`).
So inside the extended view, `api` is resolved as `cloud.backend.api` automatically, and you can use the short name without repeating the full FQN.

`include * -> cloud.backend` adds all incoming relationships targeting `cloud.backend` from anywhere else in the model.
# Detail View with Scope Inheritance and Relationship Predicate

## DSL

```likec4
view detail extends backend-overview {
  include api
  include -> cloud.backend
}
```

## Explanation

### 1. Extending `backend-overview`

`extends backend-overview` makes `detail` inherit all predicates from the parent view. It starts with everything already included by `backend-overview` (i.e., `include *` scoped to `cloud.backend`), then the body adds further predicates on top.

### 2. Scope inheritance and `include api`

The parent view is declared as `view backend-overview of cloud.backend`. The `of cloud.backend` clause sets the **view scope** to that element. When you extend this view, the derived view inherits that scope.

Within a scoped view, unqualified element names are resolved relative to the scope element. So `api` is looked up as a child of `cloud.backend`, resolving to `cloud.backend.api` — you do not need to write the full FQN. This is scope inheritance: the child element lookup context is inherited from the parent view's `of` declaration.

### 3. Incoming relationships — relationship predicate

```likec4
include -> cloud.backend
```

The arrow predicate `-> <target>` means *"include all elements that have a direct relationship pointing to `<target>`"*. This pulls in every element from the rest of the model that sends a relationship to `cloud.backend`, along with the relationships themselves. The full FQN is required here because this predicate reaches outside the scoped subtree.
