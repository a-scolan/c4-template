`styles { ... }` fails because `styles` is **not** an allowed top-level statement in LikeC4.

Allowed top-level blocks are: `import`, `specification`, `model`, `deployment`, `views`, and `global`.

To keep the same intent (set dark theme), put styling under a valid top-level `global` block:

```likec4
global {
  styles {
    theme dark
  }
}
```