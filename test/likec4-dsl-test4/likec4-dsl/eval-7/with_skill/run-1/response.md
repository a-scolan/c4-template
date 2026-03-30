## DSL

```likec4
view detail extends backend-overview {
  include api
  include -> cloud.backend
}
```

## Explanation

### (1) `extends backend-overview`

`view detail extends backend-overview` inherits all rules from the parent view — including its `include *` rule, its scope (`of cloud.backend`), and any style rules. New rules in `detail` are applied on top of the inherited ones.

### (2) `include api` — scope inheritance

When a view extends a scoped base view (`of cloud.backend`), it inherits that scope. Within a scoped view, unqualified identifiers are resolved relative to the scope element. So writing `include api` is valid because the inherited scope is `cloud.backend`, and LikeC4 resolves `api` as `cloud.backend.api` without requiring the full FQN. Writing `include cloud.backend.api` would also work but is redundant here.

**Scope inheritance** means the child view `detail` has the same `of cloud.backend` scope as `backend-overview`. Inside that scope, single-segment names like `api`, `db`, etc. are looked up as direct children of `cloud.backend` first, before falling back to global FQN resolution — exactly like lexical scoping in a programming language.

### (3) `include -> cloud.backend` — incoming relationship predicate

The relationship predicate `-> cloud.backend` selects all relationships in the model that target `cloud.backend`, regardless of where the sources come from. LikeC4 adds both the matching relationships and their source elements to the view. This is the standard form for "all incomers to a specific element from the rest of the model."
