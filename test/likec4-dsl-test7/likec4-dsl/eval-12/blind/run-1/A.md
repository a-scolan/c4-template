1. **Support status (explicit):**
   - `include * with { color red }` in a **deployment view**: **Not supported**.
   - `global style myTheme` in a **deployment view** body: **Not supported**.

2. **Supported alternative (separate construct):**
   Use a local `style` rule inside the deployment view. This is a **separate, supported deployment-view construct** (not `with { ... }` on `include`, and not `global style ...`).

3. **Minimal corrected snippet (deployment-view syntax):**

```likec4
deployment view prod {
  include *

  style * {
    color red
  }
}
```