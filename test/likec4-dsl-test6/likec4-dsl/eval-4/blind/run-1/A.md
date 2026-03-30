(1) This styling belongs in the view definition itself (i.e., view-local styling), not in the model or specification.

(2)
```likec4
view backend-focus of cloud {
  include *

  style * {
    color muted
  }

  style cloud.backend.* {
    color primary
  }
}
```