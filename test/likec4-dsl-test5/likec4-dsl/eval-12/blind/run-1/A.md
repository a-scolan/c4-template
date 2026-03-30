1) Support status

- `include * with { color red }`: **Not supported** in deployment views.
- `global style myTheme`: **Not supported** as a deployment-view construct.

2) Alternative

Use a deployment-view local `style` rule (separate supported construct), not `with { ... }` and not `global style ...`.

3) Minimal corrected snippet

```likec4
views {
  deployment prod {
    view v {
      include *

      style * {
        color red
      }
    }
  }
}
```# Styling in `deployment view`: `with { ... }` and `global style`

## Part 1 — Support status of each construct

### `include * with { color red }`

**Not supported** in `deployment view`.

The `with { ... }` inline style block on an `include` predicate is a feature of **element views** only. In a deployment view, the `include` statement accepts predicates to select deployment nodes and instances, but does not accept a trailing `with { ... }` style override block. Writing `include * with { color red }` inside a deployment view will produce a parse/validation error.

### `global style myTheme`

**Not supported** — as a view-level directive, in any view type.

`global style` (or named theme references) are **global-scope** declarations defined outside any view, typically in a shared spec or global configuration file. There is no `global style myTheme` directive you can write *inside* a view body (element or deployment) to activate a named theme. Attempting to write it inside a deployment view is not valid LikeC4 syntax.

---

## Part 2 — The local `style` rule as an alternative

Inside a `deployment view`, LikeC4 supports a **local `style` rule** as a separate, first-class construct:

```
style <selector> {
  color <value>
  shape <value>
  ...
}
```

This is **not** the same as a `with { ... }` inline block on `include`, and it is **not** the same as `global style`. It is a distinct deployment-view-level construct that applies styling to the matched nodes within that specific view only. It is the correct and supported way to apply colors and other visual properties to deployment nodes and instances inside a deployment view.

---

## Part 3 — Minimal corrected snippet

```likec4
deployment view ProductionDeployment {
  title "Production Deployment"

  include *

  // Supported: local style rule — applies red color to all included nodes
  style * {
    color red
  }
}
```

**What was removed/replaced:**
- `include * with { color red }` → split into `include *` + a separate `style * { color red }` rule (the only supported form in deployment views).
- `global style myTheme` → removed entirely; there is no valid deployment-view directive to invoke a global named style inline.
