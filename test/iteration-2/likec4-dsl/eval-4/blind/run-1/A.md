Keep this styling in the **view** (not model/spec), because it is view-specific presentation.

```likec4
view backend-focus {
  include *
  style * { color muted; opacity 30% }
  style cloud.backend.* { color primary; opacity 100% }
}
```