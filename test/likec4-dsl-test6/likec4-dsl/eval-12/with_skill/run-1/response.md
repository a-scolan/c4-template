1. `include * with { color red }` is **not supported** in a `deployment view`.
2. `global style myTheme` is **supported** in a `deployment view`, as long as `myTheme` is a `styleGroup` defined in a `global { ... }` block.
3. If you want inline styling in the deployment view, use a separate `style` rule such as `style * { color red }`; that is a different supported deployment-view construct, not `with { ... }` and not `global style`.

Minimal corrected snippet:

```likec4
global {
  styleGroup myTheme {
    style * { color red }
  }
}

views {
  deployment view infra {
    include *
    global style myTheme
  }
}
```