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
- `autoLayout LeftRight` — explicitly requested left-to-right direction.
- `rank source` on `user` — single obvious initiating anchor pulled to the left.
- `rank sink` on `database` and `mailService` — two known exit points stabilized on the right.
- `navigateTo webApp_details` — preserves the existing drill-down (assumes `webApp_details` is a stable, existing view ID).

**What this does NOT do:**
- Does not change which elements are included (structure stays as-is).
- Does not add or remove relationships.
- Does not invent the drill-down target view.

> If `webApp_details` does not yet exist, or if included elements need to change, hand off to `design-view` first.
