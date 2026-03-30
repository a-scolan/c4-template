(1) This styling belongs in the **view definition** itself (the `.c4` views file), not in the model elements or the `specification` block.

(2) Minimal view snippet:

```likec4
view highlighted_backend {
  include *

  style * {
    color muted
  }

  style cloud.backend.* {
    color primary
  }
}
```
