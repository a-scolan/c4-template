This styling belongs in the **view definition** (view-level rules), not in the model or specification.

```likec4
views {
  view backend-focus {
    include *
    style * { color muted }
    style cloud.backend.* { color primary }
  }
}
```