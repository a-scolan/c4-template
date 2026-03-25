That styling should live in the **view**, not in `model`/`specification`, because you want it only in one diagram.

```likec4
views {
  view backend-focus {
    include *

    style cloud.backend.* {
      color primary
      opacity 100%
    }

    style * {
      color muted
      opacity 40%
    }
  }
}
```

This keeps the model/spec semantics clean and applies the highlight/muted effect only for this specific view.