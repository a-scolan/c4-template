1. This styling belongs in the view definition, because it is view-specific presentation and should not be moved into the model or specification.

2.
```likec4
view backend-focus {
  include *

  style * {
    color muted
  }

  style cloud.backend.* {
    color primary
  }
}
```