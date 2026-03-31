1. **Support status**
   - `include * with { color red }` in a `deployment view`: **No — do not use this as the deployment-view styling form.**
   - `global style myTheme` in a `deployment view`: **No — treat this as unsupported for this deployment-view styling fix.**

2. **Supported alternative**
   If you want to style nodes in a deployment view, use a **separate local `style ... { ... }` rule inside that `deployment view`**. That is the supported deployment-view construct here — **not** `with { ... }` on `include`, and **not** `global style ...`.

3. **Minimal corrected snippet**

```likec4
views {
  deployment view prod {
    include prod.**
    style prod._ { color red }
  }
}
```
