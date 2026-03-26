Do not put everything into one shared bucket.

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