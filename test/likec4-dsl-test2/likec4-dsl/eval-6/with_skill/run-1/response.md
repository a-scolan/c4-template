Use `cloud.backend._`. It selects only the direct children of `cloud.backend` that already have at least one relationship with the elements accumulated in the view — exactly what you want.

Minimal snippet:

```likec4
view backend_view of cloud.backend {
  include *              // adds cloud.backend + its direct children and their mutual relationships
  include cloud.backend._ // adds only the direct children that connect to what is already included
}
```

What the other two would have selected instead:

- `cloud.backend.*` — selects ALL direct children of `cloud.backend`, regardless of whether they have any relationship with the accumulated result. Use this when you want to show all children unconditionally.
- `cloud.backend.**` — selects ALL descendants of `cloud.backend` (children, grandchildren, etc.) that have at least one relationship with the accumulated result. The difference from `_` is the recursion depth: `**` goes arbitrarily deep, `_` stops at the immediate children level.
