# Customize C2 View: External Link and Stable Drill-Down

Based on the `customize-view` skill, here is the proposed block:

```likec4
views 'C2' {
  view containers_c2 {
    include *

    link https://docs.internal/spec 'System specification'

    include webApp with {
      navigateTo webApp_details
    }
  }
}
```

**What this does:**
- `link https://docs.internal/spec 'System specification'` — attaches an external documentation link to the view using HTTPS with a descriptive label, as required by the skill.
- `include webApp with { navigateTo webApp_details }` — adds a drill-down link from the web application to its existing detail view. The target ID `webApp_details` must already exist and be stable.

**What this does NOT do:**
- Does not change which elements are included in the view.
- Does not create the `webApp_details` view — that view must pre-exist. If it does not, hand off to `design-view`.
- Does not alter element styling or layout.

Replace `https://docs.internal/spec` with your actual documentation URL and `webApp_details` with the real view ID.
