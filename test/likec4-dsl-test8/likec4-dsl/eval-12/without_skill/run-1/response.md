1. **Support status**
   - `include * with { color red }`: **Not supported** in a `deployment view`.
   - `global style myTheme`: **Not supported** as a deployment-view styling construct.

2. **Supported alternative**
   - If you want to style nodes inside a `deployment view`, use a local `style` rule **inside that deployment view**. That local `style` rule is a **separate supported deployment-view construct**; it is **not** `with { ... }`, and it is **not** `global style`.

3. **Minimal corrected snippet**

```likec4
deployment view myView {
  include *
  style * {
    color red
  }
}
```