1. **Support status**
   - `include * with { color red }`: **Yes, supported** in a deployment view as a customize-predicate form of `include`.
   - `global style myTheme`: **Yes, supported** in a deployment view, provided `myTheme` is a `styleGroup` defined in `global { ... }`.

2. **Separate alternative if you want it**
   - A local deployment-view rule such as `style * { color red }` is also supported, but it is a **different deployment-view construct**. It is **not** the same thing as `with { ... }`, and it is **not** `global style myTheme`.

3. **Minimal corrected snippet**

```likec4
global {
  styleGroup myTheme {
    style * { color red }
  }
}

views {
  deployment view prod_deploy {
    include prod.** with { color red }
    global style myTheme
  }
}
```