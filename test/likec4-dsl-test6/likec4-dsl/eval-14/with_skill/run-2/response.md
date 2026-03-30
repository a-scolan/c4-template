`styles { theme dark }` fails because `styles` is not a valid top-level LikeC4 DSL statement. Only top-level `import`, `specification`, `model`, `deployment`, `views`, and `global` blocks are allowed.

A minimal valid `.c4` alternative, using only allowed DSL top-level statements for styling inside DSL scope, is:

```likec4
global {
  styleGroup darkTheme {
    style * { color slate }
  }
}

views {
  view index {
    include *
    global style darkTheme
  }
}
```

If the intent is a project-level dark theme, put it in `likec4.config.json` instead:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "my-project",
  "styles": {
    "theme": "dark"
  }
}
```
