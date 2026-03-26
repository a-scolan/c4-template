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

**Rationale:**
- `autoLayout LeftRight` alone is often sufficient — it tells the layout engine to arrange elements in a left-to-right flow.
- Adding `rank source` on `user` provides one stable, obvious anchor so the initiating element does not drift to the center or right.
- The skill recommends against stacking `rank source` + `rank sink` + `rank same` across many elements, as this frequently produces brittle layouts.

**If the view still looks off after this:**  
Do not add more `rank` hints. Instead, consider simplifying the view structure by using `design-view` to reduce noise — a cleaner structure is more reliably rendered than a heavily rank-constrained one.
