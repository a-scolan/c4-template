1. This styling belongs in the **view definition**, because it is a view-specific presentation concern and should not be moved into the model or specification.

2. ```likec4
view cloud_overview of cloud {
  include *

  style * {
    color muted
  }

  style cloud.backend.* {
    color primary
  }
}
```