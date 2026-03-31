`styles { theme dark }` fails for two separate reasons:

1. `styles` is **not** an allowed top-level LikeC4 DSL statement. At the top level, only `import`, `specification`, `model`, `deployment`, `views`, and `global` are allowed.
2. `theme dark` is **not** valid `.c4` DSL syntax. Theme selection is a configuration concern, not a DSL block statement.

A minimal valid `.c4` alternative for styling **inside DSL scope** is to use a `views` block with a `style` rule:

```likec4
views {
  style * { color primary }

  view index {
    include *
  }
}
```

If the real intent is a **project-level dark theme**, put that in `likec4.config.json`, not in a `.c4` file:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "my-project",
  "styles": {
    "theme": "dark"
  }
}
```