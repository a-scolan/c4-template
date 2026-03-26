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

**Notes:**
- `link` with HTTPS and a human-readable label follows the skill's requirement for trusted, maintained URLs.
- `navigateTo webApp_details` references the stable existing view ID for the web application detail view.
- No element additions or removals — this is a pure enrichment of an existing, structurally correct view.

If `webApp_details` does not already exist, do not proceed with this block — create the detail view using `design-view` first, then apply this customization.
