`styles { ... }` fails in a `.c4` file because `styles` is **not** a valid top-level LikeC4 DSL statement. In DSL files, the allowed top-level statements are only `import`, `specification`, `model`, `deployment`, `views`, and `global`.

`theme dark` also is **not** a DSL statement inside `.c4` scope. Theme selection belongs in the **project config**, not in a DSL file.

## 1) Minimal valid `.c4` alternative for styling inside DSL scope

Use an allowed top-level block such as `views` and put a valid `style` rule inside it:

```likec4
views {
  style * { color primary }

  view index {
    include *
  }
}
```

That is valid because:
- `views { ... }` is an allowed top-level DSL block
- `style ... { ... }` is valid **inside** `views`
- it performs styling in DSL scope without inventing a `styles` top-level block

## 2) Minimal `likec4.config.json` snippet for a project-level dark theme

If the real intent is to set the project theme to dark, put it in config instead:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "my-project",
  "styles": {
    "theme": "dark"
  }
}
```

In short: **DSL styling goes inside `views`/`global` constructs; project theme selection goes in `likec4.config.json`.**