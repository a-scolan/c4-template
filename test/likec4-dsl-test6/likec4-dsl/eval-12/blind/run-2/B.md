1. **Support status**
   - `include * with { color red }`: **Not supported** as a deployment-view styling form. In deployment views, styling is done with a separate `style ... { ... }` rule, not by attaching `with { ... }` to `include`.
   - `global style myTheme`: **Supported**, as long as `myTheme` is a `styleGroup` defined in a `global { ... }` block.

2. **About the local `style` alternative**
   - A local `style` rule is a **separate supported deployment-view construct**.
   - It is **not** the same thing as `include ... with { ... }`.
   - It is also **not** the same thing as `global style myTheme`, which applies a reusable global style group.

3. **Minimal corrected snippet**

```likec4
views {
  deployment view infra {
    include prod.**
    style * { color red }
  }
}
```
