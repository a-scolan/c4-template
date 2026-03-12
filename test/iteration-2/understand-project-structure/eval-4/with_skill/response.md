To contribute safely here, learn the local LikeC4 conventions before thinking in UML or ArchiMate terms.

## Local conventions to understand first

- **Project layout**
  - Shared taxonomy lives in `projects/shared/`
  - Example or working projects live under `projects/template/` and `projects/spec-showcase/`
  - Skill guidance lives under `.github/skills/`
- **Naming is PascalCase and taxonomy-driven**
  - Examples: `Actor_Person`, `System_External`, `Container_Api`, `Node_Environment`
- **C4 levels are distinct**
  - C1 = actors and systems
  - C2 = runtime containers
  - C3 = internal `Component` structure inside selected containers
- **Views are organized by intent**
  - `views 'C1'`, `views 'C2'`, `views 'C3'`, `views 'Use Cases'`, `views 'Deployment'`

## Real sources of truth in this repository

Start here, in this order:

1. `projects/shared/SPEC_CHEATSHEET.md` for fast orientation
2. Shared specs for the actual legal taxonomy:
   - `projects/shared/spec-context.c4`
   - `projects/shared/spec-containers.c4`
   - `projects/shared/spec-components.c4`
   - `projects/shared/spec-global.c4`
   - `projects/shared/spec-deployment.c4`
3. The active project's `likec4.config.json`
4. The active project's current model and view files
5. `read-project-summary` to confirm the project inventory and current structure

## Taxonomy examples actually used here

- Valid container kind: `Container_Api`
- Other container kinds already defined: `Container_Webapp`, `Container_Database`, `Container_Queue`
- Valid model relationships: `uses`, `calls`, `async`, `reads`, `writes`
- Example from the template project: `mySystem.api = Container_Api 'API Server'`

## Recommended handoff

After this preflight, hand off to **`c4-modeling-process`**.

Why that next skill:
- this skill establishes workspace context and local rules
- `c4-modeling-process` then sequences the work correctly from **C1 → C2 → C3**

After that, if you are making a concrete edit, hand off again to a focused editing skill such as `create-element`, `create-relationship`, or `design-view`.

In short: learn the repository's taxonomy first, then model top-down. That is the safest way to avoid importing UML habits that do not match this LikeC4 workspace.