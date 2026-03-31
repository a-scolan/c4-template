- The base include set is the scoped element itself plus its **direct children**: in `view backend of cloud.backend { include * }`, `*` includes `cloud.backend` and every element nested immediately inside `cloud.backend` in that scope.
- From that base set, LikeC4 can still show neighboring/derived context by auto-showing relationships touching the included elements, which may make external source/target elements visible as connected neighbors, and it can also surface nested relationships implied by the included scoped content.

```likec4
view backend of cloud.backend {
  include *
  include incoming *
  include outgoing *
}
```