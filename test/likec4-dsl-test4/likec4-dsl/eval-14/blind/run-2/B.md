# Why `styles { theme dark }` fails

The `styles` block in LikeC4 DSL is used to define **element style rules** — it applies visual overrides (color, shape, icon, etc.) to elements matching a selector. It does **not** accept a `theme` keyword as a child statement. `theme` is not a valid property inside a `styles { }` block, so the parser will reject this with a syntax error.

## (1) Minimal valid `.c4` alternative for styling inside the DSL

If the intent is to customise the look of elements (e.g. apply a colour palette or shape to all elements of a given kind), use `styles` with proper element selectors and style properties:

```likec4
views {
  style * {
    color secondary
  }
}
```

`style` rules live inside a `views { }` block (or inside a specific `view` block), not in a standalone `styles { }` top-level block. A minimal valid example that changes the default color of all elements globally:

```likec4
views {
  style * {
    color muted
  }
}
```

There is no `theme dark` statement in the LikeC4 DSL — theme selection is a project/tooling-level concern, not a model-level one.

## (2) `likec4.config.json` snippet for a project-level dark theme

Theme preference is configured at the project level via `likec4.config.json`:

```json
{
  "theme": "dark"
}
```

Place this file at the root of your LikeC4 project (next to your `.c4` source files). This tells the LikeC4 renderer/CLI to use the dark colour theme when generating diagrams, without needing any DSL change in your model files.
