`styles { ... }` fails because `styles` is **not a valid top-level LikeC4 DSL statement**. In DSL files, the parser only accepts specific top-level blocks, and `theme dark` is **not a DSL directive** there either.

So this is invalid for two separate reasons:

1. `styles` is not an allowed top-level block in a `.c4` file.
2. `theme dark` is a **configuration concern**, not a DSL statement.

## Minimal valid `.c4` alternative

If the goal is to style things **inside DSL scope**, use an allowed top-level block such as `global`, and put a valid style rule inside it:

```likec4
global {
  style * {
    color #ffffff
    background #1e1e1e
  }
}
```

That is a minimal valid styling example in DSL scope.

## Minimal `likec4.config.json` alternative

If the real intent is a **project-level dark theme**, put that in config instead:

```json
{
  "theme": "dark"
}
```
