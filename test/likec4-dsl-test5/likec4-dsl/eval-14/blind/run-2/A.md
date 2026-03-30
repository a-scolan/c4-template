`styles { theme dark }` fails because `styles` is not a valid top-level DSL block in `.c4` files, and `theme dark` is not a DSL statement there. Theme selection is configured in project config, not in that DSL form.

1) Minimal valid `.c4` styling alternative (DSL scope)

```likec4
global {
  style * {
    color '#e6edf3'
  }
}
```

2) Minimal `likec4.config.json` snippet for project-level dark theme

```json
{
  "theme": "dark"
}
```
# Why `styles { theme dark }` Fails

## Explanation

The snippet fails because `theme` is **not a valid statement inside the `styles { }` block**.

In LikeC4 DSL, the `styles` top-level block only accepts **element style rules** — i.e., rules that target elements by kind, tag, or wildcard selector and assign properties like `color`, `shape`, `icon`, etc. The keyword `theme` is not recognized as a valid inner statement of `styles {}`, so the parser will reject it with a syntax error.

The `styles` block grammar looks like:

```
styles {
  element <selector> {
    color   <value>
    shape   <value>
    icon    <value>
    ...
  }
}
```

There is no `theme` keyword anywhere in the `.c4` DSL scope.

---

## (1) Minimal Valid `.c4` Alternative

If the intent is to apply a visual style globally via DSL, use an element wildcard rule inside `styles`:

```likec4
styles {
  element * {
    color secondary
  }
}
```

This is the closest DSL-level equivalent — it overrides the default color for all elements. There is no mechanism within `.c4` files to switch the overall UI theme (dark/light); that is a project-configuration or viewer concern.

---

## (2) Minimal `likec4.config.json` for a Project-Level Dark Theme

The project-level theme is declared in `likec4.config.json`:

```json
{
  "name": "my-project",
  "theme": "dark"
}
```

This instructs the LikeC4 renderer/viewer to use the dark color theme for the entire project, independently of any element style rules defined in `.c4` files.
