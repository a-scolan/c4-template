1) This styling belongs in the specific view definition (view-level styles), not in the model or specification.

2)
```likec4
view cloud_overview {
  include *

  style * {
    color muted
  }

  style cloud.backend.* {
    color primary
  }
}
```