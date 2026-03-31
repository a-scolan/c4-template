1. **Support status**
   - `include * with { color red }`: **Supported** in a `deployment view` (customized include predicate).
   - `global style myTheme`: **Supported** in a `deployment view` **if** `myTheme` is a defined `styleGroup` in `global { ... }`.

2. **Alternative clarification**
   - A local `style ... { ... }` rule is a **separate supported deployment-view construct**.
   - It is not the same as `include ... with { ... }` (predicate customization) and not the same as `global style ...` (reusing a global style group).

3. **Minimal corrected snippet**

```likec4
global {
  styleGroup myTheme {
    style * { color blue }
  }
}

views {
  deployment view infra {
    include * with { color red }
    global style myTheme
  }
}
```