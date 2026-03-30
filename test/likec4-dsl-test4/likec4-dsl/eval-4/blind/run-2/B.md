# Answer

## Part 1 — Where this styling belongs

This styling belongs inside the **view-level style rules** (within the view block itself), not in the model, specification, or any global block.

## Part 2 — Minimal view snippet

```likec4
view backend-highlighted {
  include *
  style * { color muted }
  style cloud.backend.* { color primary }
}
```

**How it works:**

- `include *` pulls all reachable elements into the view.
- `style * { color muted }` mutes every element.
- `style cloud.backend.* { color primary }` then overrides that for the direct children of `cloud.backend` only, highlighting them. Rule order matters: each subsequent `style` rule applies on top of previous ones, so the second rule wins for the matched elements.
