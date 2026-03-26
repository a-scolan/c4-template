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

**What this does:**
- Style predicates use only `muted` and `primary` from the shared spec — no custom palette entries.
- The `navigateTo` target (`webApp_details`) must already exist as a stable view ID.
- The `link` satisfies the HTTPS + descriptive-label requirement from the skill.

## Where This Skill Stops

The `customize-view` skill is scoped to **visual and navigational polish only**. It stops when:

1. **The drill-down target doesn't exist** — `design-view` must create `webApp_details` first.
2. **Included elements need to change** — structural in/out decisions belong to `design-view`.
3. **A new color or shape is required** — must go to `spec-global.c4` (with user permission) rather than a one-off inline definition.
4. **Temporal or sequence behavior is needed** — use `create-sequence-view` instead.

Summing up: apply this block to an already-structurally-correct view; for anything that alters what's in the view, use `design-view` first.
