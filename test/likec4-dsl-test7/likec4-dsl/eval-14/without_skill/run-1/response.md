`styles { theme dark }` fails because `styles` is **not a valid top-level statement in `.c4` DSL**. In LikeC4 DSL, styling inside model files must be declared under allowed DSL scopes (for example `global` with `style ...` rules), while `theme dark` is a **project config concern**, not a DSL top-level block.

### 1) Minimal valid `.c4` alternative (DSL-side styling)

```likec4
global {
  style * {
    color "#E5E7EB"
  }
}
```

### 2) Minimal `likec4.config.json` snippet (project-level dark theme)

```json
{
  "styles": {
    "theme": "dark"
  }
}
```
