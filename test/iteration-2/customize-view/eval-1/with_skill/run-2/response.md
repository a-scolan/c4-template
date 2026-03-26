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

**Rationale:**
- `style *` with low opacity globally de-emphasizes all elements.
- A second style predicate targeting API elements restores full visibility using `primary`, a color defined in `spec-global.c4`.
- No custom palette entries or hex values are introduced — fully consistent with the shared spec constraint.

**Alternative if API elements carry a tag:**
```likec4
style element.tag = #api { color primary; opacity 100% }
```

Using a tag predicate is more robust when the element names may vary.

**Scope:** This is a visual-only change. The structure of the view (included elements, relationships) is untouched.
