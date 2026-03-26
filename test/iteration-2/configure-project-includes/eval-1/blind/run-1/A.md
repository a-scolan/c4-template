Use a progressive split that preserves behavior at each step.

Recommended target layout:
- `model/context.c4` → C1 actors/systems
- `model/containers.c4` → C2 containers
- `model/components.c4` → C3 components
- `model/use-cases.c4` → use case narratives / dynamic interactions
- `model/deployment.c4` → deployment nodes + instances
- `model/operations.c4` → operational concerns (schedules, batch, observability notes if modeled)
- `views/context-views.c4` → C1 views
- `views/container-views.c4` → C2 views
- `views/component-views.c4` → C3 views
- `views/use-case-views.c4` → dynamic/use-case views
- `views/deployment-views.c4` → deployment views

Progressive migration plan:
1. Create files and copy blocks from `system.c4` without changing identifiers.
2. Move only C1 definitions + related views first; verify.
3. Move C2, then C3, verifying after each move.
4. Move deployment and operation-specific sections.
5. Keep a temporary compatibility file that just includes/redirects until migration is complete.
6. Final pass: remove duplicates and dead references.

Key rule: never change IDs while splitting; move text, then refactor names later if needed.A safe progressive split for a 1200-line `system.c4` is:

1. Freeze behavior first
- Do not rename ids during split.
- Move blocks without changing semantics.

2. Create a clean project baseline
- `projects/payments/likec4.config.json`
- `projects/payments/model/`
- `projects/payments/views/`

3. Split model definitions by abstraction
- `model/context.c4` → C1 actors + external/internal systems
- `model/containers.c4` → C2 containers and container relationships
- `model/components.c4` → C3 components and component relationships
- `model/use-cases.c4` → use-case/scenario elements (if modeled as elements)
- `model/deployment.c4` → deployment nodes/instances
- `model/operations.c4` → operational/runtime/supporting elements

4. Split views by audience
- `views/context-views.c4` → C1 views
- `views/container-views.c4` → C2 views
- `views/component-views.c4` → C3 views
- `views/use-case-views.c4` → use-case-focused views
- `views/deployment-views.c4` → infrastructure/runtime views
- `views/operations-views.c4` → operations/runbook-style views

5. Wire shared baseline in config
- Keep `include.paths` with `../shared` first.
- Keep existing `imageAliases`; add only missing aliases.

6. Migrate in slices
- Move one section at a time (C1 → C2 → C3 → deployment → ops/views).
- Validate after each move.

Result: same model behavior, clearer ownership, and easier long-term maintenance.