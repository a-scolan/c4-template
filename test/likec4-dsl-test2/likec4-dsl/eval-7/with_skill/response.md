DSL:

```likec4
views {
  view backend-overview of cloud.backend {
    include *
  }

  view detail extends backend-overview {
    title "Backend Detail"
    include api
    include * -> cloud.backend
  }
}
```

Explanation:

`view detail extends backend-overview` inherits all rules from `backend-overview`, including its `of cloud.backend` scope anchor. In LikeC4, a scoped view (`of ELEMENT_ID`) sets the lexical scope for identifier resolution inside that view body. Because `detail` extends the scoped view, it also operates inside that same `cloud.backend` scope. This is scope inheritance: the child view does not need to repeat `of cloud.backend` — the scope is carried over from the parent. So `include api` resolves as `cloud.backend.api`, not a hypothetical top-level `api`.

The relationship predicate `include * -> cloud.backend` uses relationship expression syntax from the predicates reference. `*` matches all elements across the model (the "rest of the model"), and `-> cloud.backend` targets `cloud.backend` as the destination. Together the predicate selects every relationship where the target is `cloud.backend`, and also brings in the source elements of those relationships — covering all incoming connections from the rest of the model.
