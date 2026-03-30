Valid as written.

A child view that `extends backend-overview` inherits the same scoped subject (`of cloud.backend`), so you do not redeclare it unless you are changing scope; you can add incoming relationships by including arrows that target `cloud.backend`.

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```# Answer

**Valid as written.**

When a view uses `extends`, it inherits the scope (`of cloud.backend`) from the parent view, so there is no need to repeat the `of` clause in the child view. The child view simply adds its own `include`/`exclude` rules on top of everything already defined in the parent. To also include elements that have incoming relationships to `cloud.backend`, use the `-> element` predicate:

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```
