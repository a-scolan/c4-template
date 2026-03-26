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

This keeps the C2 explicit and provides clear drill-down from the web application.# Design View – Eval 0 – Without Skill – Run 3

## Task

Design a system context (C1) view that displays all actors and systems in the model, using appropriate `include` predicates and a sensible automatic layout.

## Response

A context view shows the system boundary: who uses the system and what external systems it interacts with. In LikeC4:

```likec4
views {
  view system_landscape {
    title 'System Landscape'
    description 'All actors and systems at context level'

    include *

    autoLayout TopBottom
  }
}
```

The `include *` predicate includes all root-level model elements. When the model contains actors and system kinds (from `spec-context.c4`), these are automatically included.

### Explicit predicate approach

```likec4
views {
  view context_explicit {
    title 'Context – Explicit'

    include element.tag == #Actor
    include element.tag == #System

    autoLayout LeftRight
  }
}
```

Using tag predicates (`element.tag == #Actor`) is more selective and aligns with the tag taxonomy defined in `spec-context.c4` and `spec-global.c4`.

### Selecting layout direction

| Direction   | Best for                          |
|-------------|-----------------------------------|
| TopBottom   | Hierarchical flows                |
| LeftRight   | Process / integration flows       |
| BottomTop   | Reverse hierarchies               |
| RightLeft   | Rare; right-to-left reading flows |

Choose `LeftRight` when showing external systems flowing into an internal one.
