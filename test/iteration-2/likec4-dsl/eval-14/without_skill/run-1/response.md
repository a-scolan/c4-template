It fails because `styles { ... }` is not a valid top-level LikeC4 statement.

Minimal valid file with the same intent (dark theme at view level):

```likec4
views {
  view overview {
    include *
    theme dark
  }
}
```