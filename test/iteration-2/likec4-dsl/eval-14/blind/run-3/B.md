It fails because `styles { ... }` is not a valid top-level statement. Allowed top-level blocks are `import`, `specification`, `model`, `deployment`, `views`, `global`.

Minimal valid equivalent intent:

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