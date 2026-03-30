# Styling in Deployment Views

## (1) Are these constructs supported?

**`include * with { color red }`** — **Not supported** in deployment views.
The `with { ... }` property override block is an element-view construct. In deployment views, `include` statements do not accept inline `with { ... }` overrides.

**`global style myTheme`** — **Not supported** as a named theme reference inside a deployment view.
There is no `global style <name>` syntax to apply a pre-defined theme by name within a deployment view (or any view). Global styles are defined in a separate `global style` block at the top level of a spec file and are applied automatically to matching element kinds — you cannot invoke them by name inside a view body.

## (2) The `style` rule as a deployment-view alternative

Inside a deployment view body, LikeC4 supports a **local `style` rule** — this is a distinct, supported deployment-view construct. It is **not** the same as `with { ... }` (element-view inline override) and **not** the same as `global style` (spec-level definition). The local `style` rule lets you target nodes by kind, tag, or wildcard and apply visual properties within the scope of that single view.

## (3) Minimal corrected snippet

```likec4
deployment view myDeploymentView {
  include *

  // Local style rule — supported deployment-view construct
  style * {
    color red
  }
}
```

This uses the local `style *` block (scoped to the view) to colour all included deployment nodes red, which is the correct way to apply colour overrides in a deployment view.
