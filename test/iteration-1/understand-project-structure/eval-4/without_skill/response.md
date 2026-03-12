## First local conventions to learn in this repository

If you are coming from UML or ArchiMate, start by learning the repository’s own taxonomy and file layout before translating concepts.

1. **Understand the repository map.**
   - `projects/shared/` contains the reusable taxonomy: element kinds, tags, relationships, deployment nodes, and shared icons.
   - `projects/template/` is the starter project structure.
   - `projects/spec-showcase/` contains working examples of the same taxonomy.
   - `README.md` explains how the template is maintained and synchronized.

2. **Know the real sources of truth.**
   - The target project’s `likec4.config.json`
   - The raw shared spec files in `projects/shared/`
   - The target project’s model and view files
   - `projects/shared/SPEC_CHEATSHEET.md` is useful for quick orientation, but the raw spec files win if there is any mismatch.

3. **Adopt the local naming conventions.**
   - Public names are PascalCase.
   - Kinds follow `Category_Subtype` patterns such as `Actor_Person`, `System_Existing`, `Container_Api`, and `Node_Vm`.
   - Relationships must use the exact defined names, for example `uses`, `calls`, `async`, `reads`, and `writes`.

4. **Separate logical and deployment taxonomies.**
   - Logical model work uses C1/C2/C3 kinds such as `System_Existing`, `Container_Api`, and `Component`.
   - Deployment work uses deployment node kinds such as `Node_Environment`, `Zone_Subnet`, `Node_Vm`, and `Infra_Fw`.
   - Do not mix deployment-only relationships into logical model views.

## Practical onboarding sequence

1. Pick the target project folder.
2. Read that project’s config.
3. Read the shared spec files that define kinds, tags, and relationships.
4. Read the project’s model and view files.
5. Confirm the intended C4 level before editing.

## What to hand off to next

After project selection, taxonomy confirmation, and file discovery are complete, hand off to the editing workflow that performs the model changes in C1 → C2 → C3 order.

That keeps repository framing separate from actual model construction, which is the safest way to contribute without breaking the existing structure.
