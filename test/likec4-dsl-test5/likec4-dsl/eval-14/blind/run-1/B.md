It fails because `styles { ... }` is not a valid top-level DSL statement. LikeC4 top-level statements are `import`, `specification`, `model`, `deployment`, `views`, and `global`.

1) Minimal valid `.c4` styling alternative (DSL scope):

```likec4
global {
  styleGroup darkish {
    style * { color muted }
  }
}

views {
  view index {
    include *
    global style darkish
  }
}
```

2) Minimal `likec4.config.json` snippet for project-level theming:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "my-project",
  "styles": {
    "theme": {
      "colors": {
        "primary": "#93C5FD",
        "secondary": "#64748B"
      }
    }
  }
}
```