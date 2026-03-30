## Detail View DSL

```likec4
view detail extends backend-overview {
  include api
  include * -> cloud.backend
}
```

## What Each Part Does

### (1) `extends backend-overview`

The `extends` keyword copies all rules from `backend-overview` into `detail`. The child view starts with `include *` already applied (inherited from the parent), and every additional rule in `detail` is layered on top. Rules order is preserved: inherited rules come first, then the new rules in `detail`.

### (2) `include api` — scope inheritance

`backend-overview` is declared `of cloud.backend`. When `detail` extends it, the **child view inherits the same `of cloud.backend` scope**. In LikeC4, a scoped view sets its target element (`cloud.backend`) as the resolution scope for bare identifiers appearing in that view's rules.

Concretely: inside `detail`, the identifier `api` is looked up as a child of `cloud.backend`, so it resolves to `cloud.backend.api`. You never need to write the full FQN `cloud.backend.api` — scope inheritance does it for you, exactly the same way the parent's `*` already means "the scoped element plus its direct children", not every element in the project.

### (3) `include * -> cloud.backend` — all incoming relationships

`* -> cloud.backend` is a **relationship predicate**:
- `*` on the left selects every element in the whole project model (unrestricted wildcard on source side).
- `-> cloud.backend` constrains the target to exactly `cloud.backend`.

The predicate adds every relationship whose target is `cloud.backend`, together with each source element that participates in such a relationship. This captures all incoming relationships from the rest of the model to the `cloud.backend` container.

> **Note on `-> cloud.backend` (short form):** The short form `-> cloud.backend` (no left-hand expression) means "from the current accumulated result to `cloud.backend`". It only picks up relationships from elements *already included* in the view. To get **all** incoming relationships across the entire model — not just from elements already on the diagram — the explicit form `* -> cloud.backend` is required.
