1) **Support status (explicit):**
- `include * with { color red }`: **Not supported** in a deployment view.
- `global style myTheme`: **Not supported** as a deployment-view styling construct.

2) **Supported alternative (separate construct):**
Use a **local `style` rule inside the deployment view**. This is a separate, supported deployment-view construct (not `with { ... }`, and not `global style ...`).

3) **Minimal corrected snippet (deployment-view syntax):**
```likec4
deployment view prod {
  include *

  style * {
    color red
  }
}
```