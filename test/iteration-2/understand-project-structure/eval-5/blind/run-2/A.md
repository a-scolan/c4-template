Short answer: **No** — `projects/spec-showcase/container-views.c4` is not authoritative taxonomy for other projects.

What to validate first before adding queue/API elsewhere:

1. Confirm active project.
2. Read project summary for that project.
3. Validate kinds and relationships from shared source of truth:
   - `projects/shared/spec-containers.c4` (e.g., `Container_Api`, `Container_Queue`)
   - `projects/shared/spec-global.c4` / cheat sheet for model relationships (`calls`, `async`, etc.)
4. Verify project include wiring (`likec4.config.json`) includes shared specs.
5. Confirm correct parent system/container boundary and FQN naming.

Why: showcase files demonstrate patterns and view composition, but taxonomy authority comes from shared specs + active project context.

Safe outcome: you avoid introducing valid-looking but semantically invalid kinds/relationships in the wrong project.