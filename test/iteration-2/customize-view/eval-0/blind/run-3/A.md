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

**Explanation:**
- `autoLayout LeftRight` is appropriate here because the user explicitly requested left-to-right flow.
- `rank source` on `user` is a single, obvious entry-point anchor — the skill recommends favoring one such hint only.
- `rank sink` on `database` and `mailService` stabilizes the two output endpoints. Two `rank sink` hints are acceptable when both are clearly named and separate exit points.
- `navigateTo webApp_details` preserves the existing drill-down link; the target view ID must already be stable.

No structural changes are made: the includes, relationships, and element membership remain untouched.
