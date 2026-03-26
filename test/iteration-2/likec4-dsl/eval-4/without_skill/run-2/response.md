Keep this in the **view** (presentation concern), not in global spec/model.

```likec4
view backend-focus {
  include *

  style * {
    opacity 20%
  }

  style cloud.backend.* {
    opacity 100%
  }
}
```