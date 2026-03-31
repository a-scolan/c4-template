`styles { ... }` fails because `styles` is **not** a valid top-level DSL block in a `.c4` file. LikeC4 only allows these top-level statements: `import`, `specification`, `model`, `deployment`, `views`, and `global`.

If you want styling **inside DSL scope**, put style rules in `views { ... }` (or in a reusable `global { styleGroup ... }`). For example:

```likec4
views {
  style * { color muted }

  view index {
    include *
  }
}
```

If the real intent is a **project-level dark theme**, that belongs in `likec4.config.json`, not in a `.c4` file:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "my-project",
  "styles": {
    "theme": "dark"
  }
}
```