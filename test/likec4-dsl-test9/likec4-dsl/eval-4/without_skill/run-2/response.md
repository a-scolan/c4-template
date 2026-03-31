1. This styling belongs in the view definition itself, not in the model or specification.

2.

```likec4
view cloud_overview {
  include *

  style * {
    color muted
  }

  style "cloud.backend.*" {
    color primary
  }
}
```