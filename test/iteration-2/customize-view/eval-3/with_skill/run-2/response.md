# Customize C2 View: API Highlighting + Drill-Down + External Link

Based on the `customize-view` skill, combining all three customizations:

```likec4
views 'C2' {
  view containers_c2 {
    include *

    style * { color muted; opacity 20% }
    style api, apiGateway { color primary; opacity 100% }

    include webApp with {
      navigateTo webApp_details
    }

    link https://docs.internal/spec 'System specification'
  }
}
```

**Explanation of each directive:**

| Directive | Purpose |
|-----------|---------|
| `style * { color muted; opacity 20% }` | De-emphasize all elements globally |
| `style api, apiGateway { color primary; opacity 100% }` | Re-emphasize API elements using shared-spec `primary` color |
| `navigateTo webApp_details` | Stable drill-down to existing detail view |
| `link https://docs.internal/spec 'System specification'` | External docs link with HTTPS and label |

## Where This Skill Stops

This skill covers: `style`, `autoLayout`, limited `rank`, `navigateTo`, and `link`.

It does **not** cover:
- Creating the `webApp_details` target view — must pre-exist (use `design-view` if not)
- Changing which elements are included or excluded
- Inventing new color definitions outside `spec-global.c4`
- Redesigning the view structure

When you reach any of those boundaries, hand off to `design-view`.
