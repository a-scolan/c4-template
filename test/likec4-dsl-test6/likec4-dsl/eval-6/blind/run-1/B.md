Use `cloud.backend._`.

```likec4
view backend-related-children of cloud.backend {
  include cloud.backend
  include cloud.backend._
}
```

- `cloud.backend._` selects direct children of `cloud.backend` that are connected (have at least one relationship with elements already in the view).
- `cloud.backend.*` would select all direct children, whether connected or not.
- `cloud.backend.**` would select all descendants recursively (children, grandchildren, etc.), not just direct connected children.