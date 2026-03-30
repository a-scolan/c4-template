This styling belongs in the view as view-level style rules, not in the model or specification.

```likec4
views {
  view backend-focus {
    include *
    style * { color muted }
    style cloud.backend.* { color primary }
  }
}
```