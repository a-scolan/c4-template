`styles { ... }` fails because `styles` is **not** a valid top-level statement in LikeC4 DSL files. Only these top-level blocks are allowed: `import`, `specification`, `model`, `deployment`, `views`, `global`.

Also, `theme dark` is a **project config** concern (in `likec4.config.*`), not a standalone top-level DSL block.

A minimal valid `.c4` file with similar intent (reusable “dark-ish” styling) is:

```likec4
global {
  styleGroup darkTheme {
    style * { color slate }
  }
}

views {
  view index {
    include *
    global style darkTheme
  }
}
```