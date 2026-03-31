1. **Support status**
   - `include * with { color red }`: **No** — this is **not supported** in a `deployment view`.
   - `global style myTheme`: **No** — this is **not supported** in a `deployment view` either.

2. **Supported alternative**
   If you want styling inside a deployment view, use a **local `style` rule inside the deployment view**. That is a **separate supported deployment-view construct**. It is **not** `with { ... }` attached to `include`, and it is **not** `global style ...`.

3. **Minimal corrected snippet**

```likec4
deployment view myDeployment {
  include *

  style * {
    color red
  }
}
```
