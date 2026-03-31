Use `cloud.backend._`.

Minimal snippet:

```likec4
view of cloud.backend {
  include cloud.backend._
}
```

Why:
- `cloud.backend._` selects **only the direct children of `cloud.backend` that have at least one relationship with elements already included in the view**.

What the others would do instead:
- `cloud.backend.*` selects **all direct children** of `cloud.backend`, regardless of whether they relate to anything already in the view.
- `cloud.backend.**` selects **all descendants recursively** (children, grandchildren, etc.), again not limited to only those connected to already included elements.
