`styles { theme dark }` fails because `styles` is not a valid top-level DSL block for setting theme in LikeC4 files.

1) Minimal valid `.c4` alternative (DSL styling only)

```likec4
global {
  style * {
    color '#dddddd'
  }
}
```

2) Minimal `likec4.config.json` snippet for project-level dark theme

```json
{
  "theme": "dark"
}
```# Why `styles { theme dark }` Fails

## The Problem

`styles` is **not a valid top-level DSL statement** in LikeC4. The allowed top-level blocks in a `.c4` file are:

- `specification { ... }` — defines element kinds, relationship kinds, tags, metadata keys
- `model { ... }` — defines elements and relationships
- `views { ... }` — defines views
- `global { ... }` — defines global/shared styles applied across all views
- `likec4lib { ... }` — (library definitions)

Additionally, even if a `styles` block were valid somewhere, `theme dark` is not valid syntax within it — `theme` is not a recognized style property; it is a project-level configuration concern, not an element styling directive.

---

## (1) Minimal Valid `.c4` Alternative

To apply styling within the DSL scope, use the `global` block with `style` rules:

```likec4
global {
  style * {
    color secondary
  }
}
```

Or, to scope styles to a specific view, use `style` inside a view definition within `views { ... }`:

```likec4
views {
  view index {
    include *

    style * {
      color muted
    }
  }
}
```

Neither of these sets a "dark theme" — color palettes and UI themes are not controlled via `.c4` DSL style rules. The DSL `style` block controls per-element visual properties (color tokens, shape, opacity, etc.).

---

## (2) Minimal `likec4.config.json` for a Project-Level Dark Theme

The UI render theme (dark/light) is a project-level configuration, not a DSL concern. Set it in `likec4.config.json`:

```json
{
  "name": "my-project",
  "theme": "dark"
}
```

This instructs the LikeC4 renderer to use the dark color theme when displaying diagrams for this project.
