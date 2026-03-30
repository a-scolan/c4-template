1) **Support status**
- `include * with { color red }`: **Not supported** in a `deployment` view.
- `global style myTheme`: **Not supported inside a deployment view body**.

2) **Supported alternative (separate construct)**
Use a local `style` rule **as its own deployment-view construct** (not `with { ... }`, not `global style`).

3) **Minimal corrected snippet**
```likec4
views {
  deployment prod {
    include *

    style * {
      color red
    }
  }
}
```