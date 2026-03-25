Use `cloud.backend._`.

Minimal snippet:

views {
  view of cloud.backend backend_related_children {
    include cloud.frontend
    include cloud.backend._
  }
}

What it does:
- `cloud.backend._` selects only the direct children of `cloud.backend` that have at least one relationship with elements already included in the view.

What the other two would select instead:
- `cloud.backend.*` selects all direct children of `cloud.backend`, whether they relate to the current view contents or not.
- `cloud.backend.**` selects all descendants of `cloud.backend` recursively (children, grandchildren, etc.), not just the direct children.

In a view already scoped `of cloud.backend`, the relative form `_` is the compact equivalent of `cloud.backend._`.
