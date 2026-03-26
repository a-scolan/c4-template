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
- `link` attaches an external URL to the view. The skill requires HTTPS and a descriptive label — both satisfied here.
- `navigateTo webApp_details` keeps the drill-down path stable. The target `webApp_details` must be an already-existing view ID.

**Skill scope boundary:**  
- Structure (includes/excludes) is untouched.
- The `webApp_details` view is not created here — only referenced. If it doesn't exist yet, use `design-view` to create it first.
- No styling or layout changes are introduced by this specific request.
