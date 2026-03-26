For a clean C2 (Container) setup with drill-down from the web application, model both a context view and a container view.

Recommended LikeC4 skeleton in `projects/template/`:

- Define participants in the model:
  - `person user`
  - `system mySystem`
  - `system externalEmailService`
- Define containers in `mySystem`:
  - `container webApp`
  - `container api`
  - `container db`
- Define relationships:
  - `user -> mySystem.webApp`
  - `mySystem.webApp -> mySystem.api`
  - `mySystem.api -> mySystem.db`
  - `mySystem.api -> externalEmailService`
- Add views:
  - C1/context: include `user`, `mySystem`, `externalEmailService`
  - C2/container: include `mySystem.*` and `externalEmailService`
  - Drill-down view: focus on `mySystem.webApp` and its direct collaborators

This keeps the C2 explicit and provides clear drill-down from the web application.# Design View – Eval 0 – Without Skill – Run 2

## Task

Design a system context (C1) view that displays all actors and systems in the model, using appropriate `include` predicates and a sensible automatic layout.

## Response

A context view in LikeC4 groups all top-level actors and systems. The simplest approach:

```likec4
views {
  view index {
    title 'System Landscape'

    include *

    autoLayout TopBottom
  }
}
```

`include *` at the root level captures every model element that has no parent — i.e., actors and systems. The `autoLayout TopBottom` directive lets the renderer position nodes.

### Filtering by kind

If only specific kinds should appear, use predicate syntax:

```likec4
views {
  view system_context {
    title 'System Context View'

    include
      element.kind == Actor_Person,
      element.kind == Actor_Staff,
      element.kind == Actor_Admin,
      element.kind == System_New,
      element.kind == System_Existing,
      element.kind == System_Legacy,
      element.kind == System_External

    autoLayout LeftRight
  }
}
```

### Key points

- Use `element.kind ==` to filter by element kind (defined in `spec-context.c4`).
- `include *` is quicker but less explicit; kind-based predicates are more maintainable as the model grows.
- The `autoLayout` direction can be `TopBottom`, `BottomTop`, `LeftRight`, or `RightLeft`.
