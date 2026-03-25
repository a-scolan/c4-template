`styles { ... }` fails because `styles` is **not** a valid top-level statement in LikeC4. Top-level blocks must be allowed roots (for example `global`, `model`, `views`, `specification`).

To express the same intent (dark theme) with valid top-level structure, wrap it in `global`:

```likec4
global {
  styles {
    theme dark
  }
}
```