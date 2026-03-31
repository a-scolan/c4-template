`styles { ... }` fails because `styles` is **not** a valid top-level LikeC4 DSL block. The DSL only allows these top-level statements: `import`, `specification`, `model`, `deployment`, `views`, and `global`. Also, `theme dark` is a **project config** concern, not a DSL top-level statement.

## 1) Minimal valid `.c4` alternative for styling inside DSL scope

```likec4
specification {
  element system
}

model {
  app = system
}

views {
  style * { color muted }

  view index {
    include *
  }
}
```

If you want reusable DSL styling, use `global { styleGroup ... }` plus `global style ...` inside `views`, not a top-level `styles {}` block.

## 2) Minimal `likec4.config.json` for a project-level dark theme

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "my-project",
  "styles": {
    "theme": "dark"
  }
}
```
