That styling belongs **in the view**, not in the model or spec. The model/spec holds structural and globally-reused styles; per-view spotlight effects are view-level `style` rules.

The skill's decision tree confirms this:
- 'Style element(s) in a view → view `style` rule'

Minimal snippet — mute everything first, then restore `cloud.backend.*`:

```likec4
views {
  view backend_spotlight of cloud {
    include *

    // 1. Mute the entire canvas
    style * {
      color muted
      opacity 30%
    }

    // 2. Highlight only cloud.backend and its children
    style cloud.backend, cloud.backend.* {
      color primary
      opacity 100%
    }
  }
}
```

Key rules from the skill:
- `style` rules cascade and accumulate in order — later rules override earlier ones.
- `cloud.backend.*` (wildcard) covers all direct and nested children.
- `color muted` + reduced `opacity` is the idiomatic dull-background pattern; `color primary` + `opacity 100%` brings the target back to full prominence.
