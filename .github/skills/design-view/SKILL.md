---
name: design-view
description: Design views with proper includes/excludes and basic layout. Use for include patterns, tag filtering, and simple rank hints. For advanced styling/navigation, use customize-view.
---

# Design LikeC4 View

Use this skill when creating or modifying visualization views.

## Best Practices

1. **Preview with MCP (RECOMMENDED):** Use LikeC4 MCP `open-view` to preview changes after editing
2. **Scoped includes:** Use `include mySystem.*` (children) or `include mySystem.**` (all descendants)
3. **Directed includes:** Use `include -> mySystem.*` (incoming) or `include mySystem.* ->` (outgoing)
4. **Avoid over-broad:** Never use `include **` or `include ** -> **`
5. **Layout hints:** Add `rank source { actors }` and `rank sink { databases }`
6. **Filtering:** Use `where tag is #Tag` to scope by tags
7. **Ordering:** Place `exclude` statements after `include` statements

## Example

```likec4
view c2_containers {
  title 'C2 / Container Overview'
  
  include user
  include mySystem.* where tag is #Service
  include externalSystem
  
  rank source { user }
  rank sink { externalSystem }
}
```
