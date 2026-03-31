`theme dark` fails here because it is **not valid LikeC4 DSL inside a `.c4` file**.

Two separate things are being mixed together:

- **DSL styling** in `.c4` files is rule-based: you define actual style rules for elements/relationships/views.
- **Theme selection** such as `dark` is a **project configuration concern**, not a DSL statement inside `styles { ... }`.

So this block is invalid because:

1. `theme` is not a recognized statement in DSL styling scope.
2. A `.c4` file must use valid top-level DSL constructs and valid style-rule syntax, not config-style theme selection.

## Minimal valid `.c4` alternative

If the intent is to style things **inside DSL scope**, use a real styling rule, for example:

```likec4
global {
  style element {
    color "#e5e7eb"
  }
}
```

This is the right kind of DSL idea: a top-level DSL block containing an actual style rule and a style property.

## Minimal `likec4.config.json` alternative

If the real intent is a **project-level dark theme**, put that in `likec4.config.json` instead:

```json
{
  "theme": "dark"
}
```

In short: **use DSL rules in `.c4` files, use `theme` in project config**.