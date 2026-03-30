# Deployment View Styling: `with { ... }` and `global style`

## Part 1 — Support status of each construct

**`include * with { color red }` — Not supported in deployment views.**
The `with { ... }` customize predicate is an element-view construct. It is listed under element view predicate syntax in the LikeC4 DSL but is not part of deployment view rules. Using it in a `deployment view` will cause a validation error.

**`global style myTheme` — Not supported in deployment views.**
`global style GROUP_IDENTIFIER` is listed explicitly under Element View Rules only. It is not available inside a `deployment view` block.

## Part 2 — Local `style` rule as alternative

A local `style` rule **is** a separately supported deployment-view construct. It is not a variant of `with { ... }` or `global style`; it is its own rule that applies style overrides to deployment nodes/instances matched by a predicate expression, and it is the correct way to style elements inside a `deployment view`.

## Part 3 — Minimal corrected snippet

```likec4
deployment view prod_deploy {
  title "Production"
  include prod.**
  style * { color red }           // local style rule — supported in deployment views
  style eu._ { color primary }    // more specific override
}
```

**Why this is correct:**
- `style * { color red }` is a local style rule native to deployment views.
- It replaces the unsupported `include * with { color red }` (customize predicate) and the unsupported `global style myTheme`.
- `include` and `style` are the two constructs confirmed to work in deployment view rules in LikeC4 DSL.
