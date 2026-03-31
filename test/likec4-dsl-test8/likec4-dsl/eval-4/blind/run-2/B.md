1. This styling belongs in the view definition, not in the model or specification.

2.

```likec4
view cloud_highlighted {
  include *

  style * {
    color muted
  }

  style cloud.backend.* {
    color primary
  }
}
```