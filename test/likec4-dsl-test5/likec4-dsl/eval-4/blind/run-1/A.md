This styling belongs in the **view rules** (inside `views`), not in the model or specification.

```likec4
views {
  view backend-focus {
    include *
    style * { color muted }
    style cloud.backend.* { color primary }
  }
}
```