Use `cloud.backend._`.

```likec4
view backend-neighbors of cloud.backend {
  include *
  include cloud.backend._
}
```

Why:
- `cloud.backend._` = direct children that have at least one relationship with already-included elements.
- `cloud.backend.*` = all direct children (relationship not required).
- `cloud.backend.**` = recursive descendants that have relationships (not only direct children).