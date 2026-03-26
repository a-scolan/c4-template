## Safe template sync

1. Create a backup point first: commit or copy the current project so you can roll back.
2. Sync in a dedicated branch rather than on top of active modeling work.
3. Refresh template-owned assets first, especially shared specifications and common config.
4. Compare project config before model files. Includes, shared paths, and aliases are the first things that can break parsing.
5. Reconcile changes in shared specs in this order: global definitions, context kinds, container kinds, component kinds, deployment kinds, then code helpers.
6. Only after the shared layer is stable, review project-owned model files and re-apply intentional local customizations.
7. Treat renamed tags, relationship kinds, colors, or element kinds as compatibility changes that need explicit review.
8. Re-render the workspace and inspect representative context, container, component, and deployment views before merging.

The safe rule is: update the common contract first, then repair project-specific modeling on top of it, never the other way around.