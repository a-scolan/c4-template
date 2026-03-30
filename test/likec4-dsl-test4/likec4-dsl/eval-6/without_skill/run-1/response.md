# Answer

Use `cloud.backend._` — the **wildcard with relationship filter**.

## Minimal snippet

```likec4
view backendView of cloud.backend {
  include cloud.backend._
}
```

## What each predicate selects

| Predicate | Selects |
|---|---|
| `cloud.backend.*` | All **direct children** of `cloud.backend`, unconditionally (whether or not they have any relationship with elements already in the view). |
| `cloud.backend._` | All **direct children** of `cloud.backend` that have **at least one relationship** with elements already included in the view. This is the "connected" wildcard — it filters to only those children that are connected to the current scope. |
| `cloud.backend.**` | All **descendants** of `cloud.backend` recursively (children, grandchildren, etc.), unconditionally — the deep wildcard. |

## Summary

- `*` = direct children, all of them
- `_` = direct children, only those connected (related) to already-included elements
- `**` = all descendants at every depth, unconditionally

So to include only the direct children that have at least one relationship with elements already in view, use `cloud.backend._`.
