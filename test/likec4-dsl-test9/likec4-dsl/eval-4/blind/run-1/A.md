1. This styling belongs inside the specific `view { ... }` as local view-level `style` rules, not in the model or specification.

2. ```likec4
views {
  view backend-focus {
    include *
    style * { color muted }
    style cloud.backend.* { color primary }
  }
}
```