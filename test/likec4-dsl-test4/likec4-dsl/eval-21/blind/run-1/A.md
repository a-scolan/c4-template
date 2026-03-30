Valid as written.

When a view uses `extends`, it inherits the parent's element scope (the `of cloud.backend` binding). The child view `backend-detail` therefore resolves `include api` against `cloud.backend` — exactly as if `of cloud.backend` were repeated — without needing to redeclare it. Re-stating `of cloud.backend` would be redundant, not required.

Smallest final snippet that also adds incoming relationships to `cloud.backend`:

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```

`include -> cloud.backend` selects all relationships pointing into `cloud.backend` (and brings in their source elements), so any external callers of the backend become visible alongside the inherited `include *` content from the parent view.
