Preflight before adding a new API container:

1) Active project check
- Run `list-projects` to confirm available projects.
- Select the intended project id.

2) Taxonomy check (authoritative)
- Run `read-project-summary` for the active project.
- Confirm `specification.elementKinds`, `specification.relationshipKinds`, and `specification.tags`.

3) Source-of-truth check
- Treat the active project's `likec4.config.json` and its included `.c4` files as authoritative.
- Treat showcase/example files as reference patterns only unless included by config.

C1 → C2 → C3 plan:
- C1 (Context): add/confirm external actors/systems and system-level relationships for the API boundary.
- C2 (Container): add the new API container in the target system and connect it to peer containers and externals using allowed relationship kinds.
- C3 (Component): decompose the API container into core components (routing/application/domain/integration) and map internal interactions.
- Then add/adjust views in the same project only, re-validating kinds/relationships before each edit.
