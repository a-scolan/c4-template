1) Support status
- `include * with { color red }`: **Not supported** in deployment views.
- `global style myTheme`: **Not supported** as a deployment-view directive.

2) Alternative
- Use a **local `style` rule inside the deployment view**. This is a separate supported deployment-view construct (not `with { ... }` and not `global style ...`).

3) Minimal corrected snippet

```likec4
views {
  deployment prod.main {
    include *

    style * {
      color red
    }
  }
}
```
# Styling in Deployment Views: `include * with { color red }` and `global style myTheme`

## (1) Support Status of Each Construct

### `include * with { color red }`

**Not supported** in deployment views.

The `with { ... }` inline override syntax (used in element views to override properties like `color`, `shape`, `title` etc. directly on an `include` statement) is **not available** in deployment views. Deployment views use a different predicate/rule syntax and do not accept `with { ... }` property blocks on `include` statements.

### `global style myTheme`

**Not supported** in deployment views.

`global style <name>` (referencing a named theme/style block defined at the global/spec level) is applicable to **element views**, not deployment views. Deployment views do not support referencing global style themes by name inside their body.

---

## (2) The `style` Rule in Deployment Views

Deployment views do support a **local `style` rule** as a first-class, documented construct. This is distinct from both `with { ... }` (an inline element-view override) and `global style <name>` (a global theme reference). The syntax is:

```
style <selector> {
  color <value>
  ...
}
```

This `style` rule targets deployment nodes or instances matched by a selector (e.g., `*`, a specific node id, or a wildcard pattern) and applies styling properties within the deployment view's scope. It is **not** a workaround — it is the **intended deployment-view mechanism** for styling.

---

## (3) Minimal Corrected Snippet

Below is a minimal deployment view that uses only supported deployment-view syntax to color nodes red:

```likec4
deployment view myDeploymentView {
  include *

  style * {
    color red
  }
}
```

**What changed from the original attempts:**
- Removed `with { color red }` from the `include` statement (unsupported in deployment views).
- Replaced `global style myTheme` reference with a local `style * { color red }` block (the supported deployment-view construct).
