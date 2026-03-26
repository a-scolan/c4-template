# Customize C2 View: Left-to-Right Flow with Rank Anchors and Drill-Down

Based on the `customize-view` skill, here is the LikeC4 block:

```likec4
views 'C2' {
  view containers_c2 {
    include *

    autoLayout LeftRight

    include user with { rank source }
    include database with { rank sink }
    include mailService with { rank sink }

    include webApp with {
      navigateTo webApp_details
    }
  }
}
```

**What this does:**
- `autoLayout LeftRight` — the user explicitly asked for left-to-right reading.
- `rank source` on `user` — one clear entry-point anchor; avoids over-constraining.
- `rank sink` on `database` and `mailService` — two named outputs stabilized on the right side.
- `navigateTo webApp_details` — keeps the existing drill-down stable; `webApp_details` must already exist.

**Scope boundary:**  
This block does not alter the list of included elements, does not create the detail view, and does not change relationships. If those need to change, use `design-view` first.
