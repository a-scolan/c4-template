1. **Support status**
   - `include * with { color red }`: **No** — do not use `with { ... }` as the styling mechanism in a `deployment view`.
   - `global style myTheme`: **No** — do not use `global style` as the deployment-view styling fix here.

2. **Supported alternative**
   - Use a **local `style ... { ... }` rule inside the `deployment view`**. That is a separate supported deployment-view construct. It is **not** `with { ... }`, and it is **not** `global style`.

3. **Minimal corrected snippet**

```likec4
views {
  deployment view prod {
    include prod.**
    style * { color red }
  }
}
```
