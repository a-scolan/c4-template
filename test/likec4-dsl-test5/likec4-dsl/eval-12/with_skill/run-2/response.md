1. `include * with { color red }`: **Not supported as the deployment-view node-styling mechanism**. `global style myTheme`: **Not supported in deployment views**.
2. A local `style` rule is a separate, supported deployment-view construct (not `with { ... }` and not `global style`).
3. ```likec4
views {
  deployment view prod_nodes {
    include *
    style * { color red }
  }
}
```