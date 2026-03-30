It fails for two separate reasons:

1. `styles { ... }` is not a valid top-level DSL block in a `.c4` file.
2. `theme dark` is not a DSL styling statement for a `.c4` model file.

Inside DSL scope, you define styling with allowed DSL constructs such as a top-level `global` block containing `style` rules. If the intent is to switch the whole project to a dark theme, that belongs in configuration, not in the `.c4` DSL file.

Minimal valid `.c4` styling alternative:

```likec4
global {
  style * {
    color red
  }
}
```

Minimal `likec4.config.json` snippet for a project-level dark theme:

```json
{
  "theme": "dark"
}
```
