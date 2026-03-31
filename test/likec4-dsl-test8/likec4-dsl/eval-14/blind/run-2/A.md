`styles { ... }` fails because `styles` is **not** a valid top-level `.c4` statement. In LikeC4 DSL, the only allowed top-level statements are `import`, `specification`, `model`, `deployment`, `views`, and `global`. So this block is rejected before `theme dark` even matters.

Also, `theme dark` is **not** a valid `.c4` DSL statement. Theme configuration belongs in `likec4.config.json` under the config-level `styles` option, not in a `.c4` file.

1. Minimal valid `.c4` alternative for styling inside DSL scope:

```likec4
views {
  style * { color muted }

  view index {
    include *
  }
}
```

2. Minimal `likec4.config.json` snippet if the intent is project-level theming:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "my-project",
  "styles": {
    "theme": {
      "colors": {
        "primary": "#7dd3fc",
        "secondary": "#94a3b8"
      }
    }
  }
}
```

So the fix is: use `views { style ... }` / `global { styleGroup ... }` for DSL-scoped styling, and use `likec4.config.json` for project-level theme settings.