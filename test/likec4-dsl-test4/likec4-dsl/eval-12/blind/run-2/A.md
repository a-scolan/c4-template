# Deployment View Styling in LikeC4

## (1) Support for `include * with { color red }` and `global style myTheme`

**`include * with { color red }`** — **Not supported** in deployment views.  
The `with { ... }` inline override syntax on `include` predicates is an element-view construct. In a deployment view, `include` accepts deployment node/instance selectors but does not support the `with { ... }` property-override block. Attempting to use it will produce a parse error.

**`global style myTheme`** — **Not supported** in deployment views.  
The `global style <name>` directive (which applies a named style preset) is scoped to element views. Deployment views do not recognise this directive; using it inside a `deployment view` block will cause an error.

---

## (2) The `style` rule in deployment views

Deployment views do support a local **`style`** rule as a first-class construct. It is written directly inside the `deployment view` block and targets deployment nodes or instances by their selector. This is **not** the same as `with { ... }` (which is an element-view inline override) and **not** the same as `global style` (which applies a named preset). It is a separate, deployment-view-specific styling mechanism.

Syntax:
```
style <selector> {
  color <value>
  // other style properties…
}
```

---

## (3) Minimal corrected snippet

```likec4
deployment view myDeploymentView {
  include *

  style * {
    color red
  }
}
```

This snippet:
- Uses `include *` without an unsupported `with { ... }` block.
- Uses the `style` rule (a supported deployment-view construct) to apply the colour, instead of `global style myTheme`.
