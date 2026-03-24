The styling should live in the **view**, not in the model or spec. Model/spec styles are global and affect every view; per-view highlighting belongs inside the `view { }` block using `style` rules. Rules are applied in order, so mute everything first, then override `cloud.backend.*`:

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

`cloud.backend.*` selects direct children of `cloud.backend`. Use `cloud.backend.**` instead if you also want all deeper descendants highlighted.
