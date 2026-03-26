Do not put everything into one shared bucket.

The clean approach is to separate shared technical specifications from shared business/domain content, while keeping the structure shallow.

A good split is:

- shared technical specs: element kinds, tags, relationships, styles, deployment nodes, colors
- shared domain models: only reusable business actors/systems/containers that are genuinely cross-project
- project folders: business models and views owned by one project

That gives you three levels, not a maze:

1. `projects/shared/specs/` or the current shared spec files for technical conventions
2. `projects/shared/domains/` for reusable business concepts
3. `projects/<project-name>/` for owned project models and views

Why this is better:

- technical conventions evolve differently from business models
- business reuse needs ownership and review, not just convenience
- projects stay readable because they include shared specs always, and shared domain bundles only when needed

Rules of thumb:

- If it defines modeling vocabulary, put it in shared specs.
- If it is a reusable business concept used by several projects, put it in a separate shared domain area.
- If one project clearly owns it, keep it in that project.
- Keep includes explicit and short.
- Keep one README or index explaining what is shared and why.

So: separate specs and domains, but keep the folder model intentionally small and predictable. Organized, not labyrinthine.Do not put everything into one shared bucket.

The cleanest approach is to separate shared specifications from shared business domains:
- shared specifications = DSL conventions, tags, colors, relationship kinds, reusable element kinds
- shared business domains = reusable actors, systems, and domain fragments that multiple projects intentionally depend on

That means the repo should stay shallow but not flat. A good mental model is:
- `projects/shared/` for technical conventions and modeling vocabulary
- a clearly named shared-domain area or domain files for reusable business models
- project folders for project-owned systems, containers, relationships, and views

Why this split works:
- specs stay stable and generic
- business models stay explicit and intentional
- projects can import what they need without making every shared file a dumping ground
- the repo stays navigable because the separation is semantic, not deeply nested

So yes, separate specs and domains. Just keep the structure small and obvious. The goal is not “everything shared”; the goal is “only the right things shared, in the right layer.”
Do not put everything into one shared bucket.

The clean approach is to separate shared technical specifications from shared business/domain content, while keeping the structure shallow.

A good split is:

- shared technical specs: element kinds, tags, relationships, styles, deployment nodes, colors
- shared domain models: only reusable business actors/systems/containers that are genuinely cross-project
- project folders: business models and views owned by one project

That gives you three levels, not a maze:

1. `projects/shared/specs/` or the current shared spec files for technical conventions
2. `projects/shared/domains/` for reusable business concepts
3. `projects/<project-name>/` for owned project models and views

Why this is better:

- technical conventions evolve differently from business models
- business reuse needs ownership and review, not just convenience
- projects stay readable because they include shared specs always, and shared domain bundles only when needed

Rules of thumb:

- If it defines modeling vocabulary, put it in shared specs.
- If it is a reusable business concept used by several projects, put it in a separate shared domain area.
- If one project clearly owns it, keep it in that project.
- Keep includes explicit and short.
- Keep one README or index explaining what is shared and why.

So: separate specs and domains, but keep the folder model intentionally small and predictable. Organized, not labyrinthine.
Do **not** put everything in shared.

A scalable split is:
- **Shared specs layer**: technical conventions, base kinds/tags/metadata rules, reusable style constraints
- **Shared domain layer (small, curated)**: only truly reusable business abstractions
- **Project domain layer**: concrete bounded-context models owned by each project

A simple rule:
- if many teams need it and it changes slowly -> shared
- if it belongs to one bounded context or changes often -> project-local

To avoid a maze:
1. keep only 2–3 top-level shared entry files
2. publish naming/import conventions
3. enforce dependency direction (project -> shared contracts, not random lateral imports)
4. document ownership per folder

This keeps reuse high without turning the repository into an unmaintainable dependency graph.