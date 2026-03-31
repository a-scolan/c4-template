`styles { ... }` fails because `styles` is **not** an allowed top-level DSL statement in `.c4` files. Allowed top-level statements are only: `import`, `specification`, `model`, `deployment`, `views`, `global`.

### 1) Minimal valid `.c4` alternative (styling inside DSL scope)

```likec4
specification {
  element service {
    style { color slate }
  }
}

model {
  api = service
}

views {
  view v {
    include api
  }
}
```

### 2) Minimal `likec4.config.json` snippet (project-level dark theme intent)

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "my-project",
  "styles": {
    "theme": "dark"
  }
}
```