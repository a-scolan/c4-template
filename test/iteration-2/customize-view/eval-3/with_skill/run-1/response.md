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

**What each part does:**
- `style * { color muted; opacity 20% }` — globally de-emphasizes all elements.
- `style api, apiGateway { color primary; opacity 100% }` — re-emphasizes API elements using `primary` from `spec-global.c4`. No custom hex colors.
- `include webApp with { navigateTo webApp_details }` — preserves drill-down; `webApp_details` must be a stable, existing view ID.
- `link https://docs.internal/spec 'System specification'` — attaches the internal docs URL with a descriptive label (HTTPS required).

## Where This Skill Stops

The `customize-view` skill stops at the edge of the current view structure. It does **not**:

- Change which elements are included or excluded from the view.
- Create the `webApp_details` view — the target must pre-exist. If it does not exist yet, use `design-view` first.
- Invent new color names or shapes outside the shared spec.
- Rebuild or redesign the view from scratch.

If the task requires changing parent context, adding new elements, or creating a new detail view, hand off to `design-view` before applying this block.
