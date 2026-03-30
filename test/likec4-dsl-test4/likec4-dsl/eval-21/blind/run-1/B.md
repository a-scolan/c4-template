Valid as written.

A view declared with `extends <parent-view>` inherits the scope of the parent view automatically, so there is no need to repeat `of cloud.backend`. The `extends` keyword causes the child view to start with all the rules (include/exclude/style) of the parent and then apply its own additional rules on top. Because `backend-overview` already carries the `of cloud.backend` scope, `backend-detail` resolves element identifiers (like `api`) within that same scope without redeclaring it.

Smallest final snippet that also adds incoming relationships to `cloud.backend`:

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```
