# Customize C2 View: Keep User on the Left Without Brittle Rank Directives

Based on the `customize-view` skill guidance ("prefer `autoLayout` before rank, favor one obvious anchor"):

```likec4
views 'C2' {
  view containers_c2 {
    include *

    autoLayout LeftRight

    include user with { rank source }
  }
}
```

**Why this is the right minimal approach:**
- `autoLayout LeftRight` sets the left-to-right reading axis so the user naturally ends up on the left.
- A single `rank source` on `user` is the one obvious anchor — it pins the initiating element without over-constraining the rest of the layout.
- No `rank sink`, no `rank same` — the skill explicitly warns that stacking multiple rank hints often produces brittle or broken views.

**When to stop here:**  
If this single pair (`autoLayout LeftRight` + `rank source` on `user`) does not fully stabilize the layout, the next step is to simplify the view structure with `design-view` rather than adding more rank hints.
