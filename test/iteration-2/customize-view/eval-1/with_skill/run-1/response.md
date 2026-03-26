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

**What this does:**
- `style *` de-emphasizes every element with the `muted` palette color at 20% opacity.
- The second predicate re-emphasizes API elements (`api`, `apiGateway`) with `primary` color at full opacity so they stand out.
- Both `muted` and `primary` are standard palette names from `spec-global.c4` — no custom colors are invented.

**Constraints respected:**
- No local hex color definitions.
- No parent context is hidden — the outer container boundary remains visible.
- The included elements are not changed; only presentation is adjusted.

> Replace `api, apiGateway` with the actual element IDs or a wildcard predicate (e.g., `element.tag = #api`) that matches the API elements in your model.
