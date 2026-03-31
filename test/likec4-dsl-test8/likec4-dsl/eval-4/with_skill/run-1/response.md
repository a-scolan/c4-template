This styling belongs in the `view` as a view-level `style` rule, not in the model or specification.

```likec4
views {
  view backend-focus {
    include *
    style * { color muted }
    style cloud.backend.* { color primary }
  }
}
```