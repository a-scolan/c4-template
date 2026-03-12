If you are coming from UML or ArchiMate, first learn how this repository defines its local LikeC4 vocabulary and workflow. That will keep you from importing outside naming habits into the model.

## Local structures to understand first

1. **`projects/shared/`**
   - This is the main source of truth for taxonomy.
   - It defines element kinds, relationship kinds, tags, colors, and deployment node kinds.

2. **`projects/template/`**
   - This is the baseline project structure.
   - It shows how a project is wired through `likec4.config.json`, `system-model.c4`, and `system-views.c4`.

3. **`projects/spec-showcase/`**
   - This is the local example/reference project.
   - Use it to see patterns and examples, not to override the shared taxonomy.

4. **`.github/skills/`**
   - This is the workflow layer.
   - It tells you which skill to use first, which skill should take over next, and what order to follow before editing.

## Real sources of truth in this repository

Use these in order:

1. **The active project `likec4.config.json`**
   - Confirms which project you are editing and which shared files are included.

2. **`read-project-summary` for the active project**
   - Confirms what the project actually loads: elements, views, kinds, and tags.

3. **Shared specs under `projects/shared/`**
   - `spec-context.c4`
   - `spec-containers.c4`
   - `spec-components.c4`
   - `spec-global.c4`
   - `spec-deployment.c4`

4. **`projects/shared/SPEC_CHEATSHEET.md`**
   - Great for onboarding and quick lookup.
   - Still secondary to the actual `spec-*.c4` files.

5. **The active project model and view files**
   - These show how the repository currently applies the taxonomy.

## Local conventions that matter here

- Use **PascalCase** taxonomy names such as `Actor_Person`, `System_Existing`, `Container_Api`, `Container_Webapp`, `Container_Database`, `Node_Environment`, `Node_Vm`.
- Use the repository’s **model relationship** vocabulary: `uses`, `calls`, `async`, `reads`, `writes`.
- Keep **deployment relationships** separate from model relationships.
- Model top-down: **C1 context → C2 containers → selective C3 components**.
- Treat C3 as optional and only add it when a container genuinely needs internal detail.
- Put interaction technology on the relationship in the system model.

## Practical orientation for this repository

- `projects/template/system-model.c4` currently shows a clean C1/C2 example with `user`, `mySystem`, `emailService`, plus `webapp`, `api`, and `database`.
- `projects/template/system-views.c4` currently organizes views under `C1` and `C2`, with drill-down navigation from context to containers.
- That means the repository already expects structured C4 progression rather than free-form diagramming.

## Best next handoff

After this preflight, hand off to **`c4-modeling-process`**.

- This skill establishes the project, taxonomy, and local rules.
- `c4-modeling-process` then sequences the work correctly as C1 → C2 → selective C3 and hands off to a more specific editing skill if needed.