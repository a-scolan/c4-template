# Deployment View Styling: `with { ... }` and `global style`

## Part 1 — Support status of each construct

**`include * with { color red }`** — **Not supported** in deployment views.  
The `with { ... }` customize-predicate form is an element-view construct. The LikeC4 predicate reference documents it for element/dynamic views; no deployment view syntax or example applies `with { ... }` on an include predicate. Using it inside a `deployment view` will produce a validation error.

**`global style myTheme`** — **Not supported** in deployment views.  
`global style GROUP_IDENTIFIER` is documented as an element-view rule. The LikeC4 reference and all canonical examples show it applied inside element views (`view ... { global style ... }`), never inside a `deployment view { ... }` block.

## Part 2 — Supported alternative

The correct alternative is a local **`style` rule** placed inside the `deployment view` block:

```likec4
style * { color red }
```

This is a **separate, independently supported deployment-view construct** — it is neither `with { ... }` (a customize predicate) nor `global style` (a global style-group application). The canonical deployment view examples from the reference confirm it:

```likec4
deployment view prod_deploy {
  include prod.**
  style eu._ { color primary }   // supported deployment-view style rule
  style us._ { color secondary }
}
```

## Part 3 — Minimal corrected snippet

```likec4
deployment view infra-overview {
  include prod.**
  style * { color red }
}
```

This stays entirely within supported deployment-view syntax:
- `include prod.**` selects all deployment nodes recursively under `prod`
- `style * { color red }` applies the red color to all included nodes using the supported `style` rule construct
