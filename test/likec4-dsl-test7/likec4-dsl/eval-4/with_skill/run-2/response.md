This styling belongs in the view as view-level `style` rules, not in the model or the specification.

```likec4
views {
  view backend-highlight {
    include *
    style * { color muted }
    style cloud.backend.* { color primary }
  }
}
```