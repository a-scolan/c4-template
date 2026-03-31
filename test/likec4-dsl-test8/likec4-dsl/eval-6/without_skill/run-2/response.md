Use `cloud.backend._`.

Minimal example:

```likec4
view backend_focus of cloud.backend {
  include cloud.backend
  include cloud.backend._
}
```

Why this one:
- `cloud.backend._` selects only the **direct children of `cloud.backend` that are connected by at least one relationship to elements already included in the view**.
- That matches your requirement: **not all children**, only the directly nested ones that actually relate to the current view content.

What the other two would do instead:
- `cloud.backend.*` selects **all direct children** of `cloud.backend`, whether they have relationships in the view or not.
- `cloud.backend.**` selects **all descendants recursively** under `cloud.backend` (children, grandchildren, deeper nested elements), not just the direct children.
