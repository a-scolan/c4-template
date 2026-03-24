Styling belongs in the **view**, not in the model or spec. Model/spec `style` blocks set element-kind defaults globally; per-view highlight overrides must live inside the view definition so they do not affect other views.

```likec4
view backendFocus of cloud {
  title 'Backend Highlighted'

  include *

  // Mute everything first
  style * {
    color muted
    opacity 30%
  }

  // Re-highlight only cloud.backend subtree
  style cloud.backend.* {
    color primary
    opacity 100%
  }
}
```

`style *` with `color muted` / low opacity greys out all visible elements; the second `style cloud.backend.*` block overrides only those elements back to full colour. The selector `cloud.backend.*` matches every direct and nested descendant of `cloud.backend`.
