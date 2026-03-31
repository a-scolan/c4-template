`theme dark` fails for two separate reasons:

1. `styles` is not a valid top-level LikeC4 DSL block in a `.c4` file. Top-level DSL statements are things like `specification`, `model`, `views`, and `global`.
2. `theme` is not a DSL styling statement. In DSL scope, you define style rules; you do not switch the project UI theme there.

So this file is mixing up two different layers:

- **DSL styling** in `.c4` files: style rules for model/view rendering
- **Project configuration** in `likec4.config.json`: project-level theme selection such as dark mode

A minimal valid `.c4` alternative, using actual DSL styling syntax, is:

```likec4
global {
  style element {
    color blue
  }
}
```

That is valid because it uses a valid top-level DSL block (`global`) and a real DSL styling rule (`style ...`).

If the intent is a project-level dark theme, the minimal `likec4.config.json` snippet is:

```json
{
  "theme": "dark"
}
```

In short: use `.c4` for style rules, and `likec4.config.json` for the project theme.