1. `include * with { color red }` is **not supported** in `deployment view`; `global style myTheme` is also **not supported** there.
2. In `deployment view`, use a **separate local `style` rule** (supported deployment-view syntax), not `with { ... }` and not `global style`.
3. Minimal corrected snippet:

```likec4
views {
  deployment view prod_nodes {
    include prod.**
    style * { color red }
  }
}
```