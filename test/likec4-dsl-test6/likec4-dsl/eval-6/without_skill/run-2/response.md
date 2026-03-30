Use `cloud.backend._`.

```likec4
view backend-direct-neighbors of cloud.backend {
  include *
  include cloud.backend._
}
```

Why this one:
- `cloud.backend._` selects only the direct children of `cloud.backend` that have at least one relationship with elements already included in the view.

What the others would do instead:
- `cloud.backend.*` would include all descendants of `cloud.backend`, recursively.
- `cloud.backend.**` would include the entire subtree of `cloud.backend` and `cloud.backend` itself.