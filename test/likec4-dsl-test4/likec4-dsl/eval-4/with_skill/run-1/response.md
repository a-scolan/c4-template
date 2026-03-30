# Answer

## Part 1 — Where this styling belongs

This styling belongs inside the **view definition itself**, as view-level `style` rules — not in the model, not in the specification, and not in a `global styleGroup`.

## Part 2 — Minimal LikeC4 view snippet

```likec4
views {
  view backend-highlight {
    include *
    style * { color muted }
    style cloud.backend.* { color primary }
  }
}
```

**How it works:**

- `include *` pulls every element reachable from the model into the view.
- `style * { color muted }` mutes all included elements first.
- `style cloud.backend.* { color primary }` overrides only the direct children of `cloud.backend` back to the highlighted `primary` color.

View-level style rules are applied in order — each subsequent `style` rule overrides the previous one for matching elements — so the dedicated `cloud.backend.*` rule wins over the blanket `*` mute rule.
