# Why `theme dark` inside `styles {}` fails

## Problem

In LikeC4 DSL, the `styles {}` block accepts only **element style rules** — i.e., rules that target element kinds or tagged elements and set visual properties (`color`, `shape`, `icon`, etc.).

`theme` is **not** a valid statement inside a `styles {}` block. It is a project-level configuration concern, not a per-element style rule. Placing `theme dark` inside `styles {}` causes a parse/validation error because the DSL grammar does not define `theme` as a legal child of the `styles` scope.

---

## (1) Minimal valid `.c4` alternative

If the intent is purely DSL-side styling (colors, shapes), the `styles {}` block should contain valid element style rules. There is no DSL-level keyword to switch a global theme; you would instead set colors on the root element kinds:

```likec4
styles {
  element * {
    color secondary
  }
}
```

This is the closest DSL-only approximation — applying a uniform color to all elements. LikeC4 does not expose a `theme dark/light` toggle inside `.c4` files.

---

## (2) Project-level dark theme via `likec4.config.json`

To configure a dark theme at the project level, add a `theme` key in the project configuration file:

```json
{
  "theme": "dark"
}
```

This is the correct place to declare theme preference; the DSL (`.c4` files) handles structural and style rules, while `likec4.config.json` handles project-level settings such as theme.
