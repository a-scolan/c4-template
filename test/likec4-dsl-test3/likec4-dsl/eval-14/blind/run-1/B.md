`styles { ... }` fails because `styles` is **not** a valid top-level statement in LikeC4 DSL. The parser only accepts specific top-level blocks (such as `specification`, `model`, `views`, etc.), so `theme dark` inside `styles` is rejected.

A minimal valid file with the same intent is:

```likec4
specification {
  theme dark
}
```