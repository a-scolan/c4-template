The proposal fails because `styles { ... }` is **not** a valid top-level DSL block in a `.c4` model file.

In LikeC4 DSL, styling-related declarations that belong inside DSL scope use the allowed top-level DSL statements such as `specification`, `model`, `views`, and `global`. A standalone `styles` block is not one of those allowed DSL statements, so the parser rejects it.

Also, `theme dark` is not expressed inside a `.c4` file as a top-level `styles` section. If the goal is to control the project theme globally, that belongs in the project configuration, not in the model DSL.

## Minimal valid `.c4` alternative

If the intent is to define styling **inside DSL scope**, use an allowed top-level block such as `global`:

```likec4
global {
  style "focused" {
    color "#ffffff"
  }
}
```

That is valid because `global` is an allowed top-level DSL statement, and styling is declared within that scope.

## Minimal `likec4.config.json` alternative

If the real intent is a **project-level dark theme**, put it in `likec4.config.json` instead:

```json
{
  "theme": "dark"
}
```

So the short version is:
- `styles { theme dark }` fails because `styles` is not a valid top-level DSL block in a `.c4` file.
- Use `global { ... }` for DSL-scoped styling.
- Use `likec4.config.json` for project-level theme selection such as dark mode.
