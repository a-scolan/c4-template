It fails because `styles { ... }` is not a valid top-level LikeC4 DSL block. Only `import`, `specification`, `model`, `deployment`, `views`, and `global` are allowed at the top level. Also, `theme dark` is not a DSL statement.

1. Minimal valid `.c4` alternative inside DSL scope:

```likec4
global {
  styleGroup darkTheme {
    style * { color slate }
  }
}
```

2. If the intent is a project-level dark theme, put it in `likec4.config.json`:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "my-project",
  "styles": {
    "theme": {
      "colors": {
        "primary": "#1f2937",
        "secondary": "#111827"
      }
    }
  }
}
```