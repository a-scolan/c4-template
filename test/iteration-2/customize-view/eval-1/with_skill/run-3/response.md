# Customize View: Highlight API Elements Using Shared-Spec Palette

The `customize-view` skill requires using only shared-spec color names — no custom hex values. Here is the proposed customization:

```likec4
views 'C2' {
  view containers_c2 {
    include *

    style * { color muted; opacity 20% }
    style api, apiGateway { color primary; opacity 100% }
  }
}
```

**Key points:**
- Only `muted` and `primary` are used — both are defined in `spec-global.c4`. No new hex colors.
- The layered style approach (global de-emphasis, then targeted re-emphasis) is the standard pattern from the skill.
- Parent context boundaries are not hidden; opacity drop applies to elements only, not to container frames.

**If API elements share a tag (e.g., `#api`):**
```likec4
style element.tag = #api { color primary; opacity 100% }
```

This is more maintainable when multiple API elements exist.

No structural changes, no new views, no includes/excludes modified.
