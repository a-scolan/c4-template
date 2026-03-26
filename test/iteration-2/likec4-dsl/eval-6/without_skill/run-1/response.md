Use `cloud.backend._`.

```likec4
view backend-related of cloud.backend {
  include cloud.backend._
}
```

- `cloud.backend._` = direct children that are relationship-connected to already included elements.
- `cloud.backend.*` = all direct children.
- `cloud.backend.**` = all descendants recursively.