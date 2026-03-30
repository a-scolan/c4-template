1. **Support status**
   - `include * with { color red }`: **Not supported** in a deployment view. `include *` is supported, but the inline `with { ... }` styling form is not.
   - `global style myTheme`: **Not supported** as a deployment-view styling construct.

2. **Supported alternative**
   If you want styling inside a deployment view, use a separate local `style` rule in that deployment view. That is a different supported construct; it is **not** the same as `with { ... }` and it is **not** `global style`.

3. **Minimal corrected snippet**
```likec4
include *
style * {
  color red
}
```
