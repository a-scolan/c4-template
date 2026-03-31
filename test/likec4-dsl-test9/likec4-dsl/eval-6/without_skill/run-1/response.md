Use `cloud.backend._`.

Minimal snippet:

```likec4
view of cloud.backend {
  include cloud.backend
  include cloud.backend._
}
```

Why:
- `cloud.backend._` selects only the **direct children of `cloud.backend` that have at least one relationship with elements already included in the view**.

What the others would select instead:
- `cloud.backend.*` selects **all direct children** of `cloud.backend`, whether they have relationships in the view or not.
- `cloud.backend.**` selects **all descendants recursively** under `cloud.backend` (children, grandchildren, etc.), not just the direct children, and not limited to only those connected to already included elements.
