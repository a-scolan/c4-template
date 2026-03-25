For a **one-view-only** highlight, keep styling in the **view**, not in `model`/`specification` (those are global defaults).

```likec4
views {
  view backend-focus {
    include *

    style * {
      color muted
    }

    style cloud.backend.* {
      color primary
    }
  }
}
```

This mutes everything in the view, then highlights only `cloud.backend.*` in that specific view.