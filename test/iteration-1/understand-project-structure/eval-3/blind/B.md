## What must be locked in before handing off to modeling work

Before any step-by-step modeling begins, this repository needs a clean workspace framing pass that locks in the following:

1. **The active project**
   - Decide whether you are modeling in `projects/template/` or `projects/spec-showcase/`.
   - Confirm the matching `likec4.config.json`.

2. **The real sources of truth**
   - Shared taxonomy in `projects/shared/spec-context.c4`, `projects/shared/spec-containers.c4`, `projects/shared/spec-components.c4`, `projects/shared/spec-global.c4`, and `projects/shared/spec-deployment.c4`
   - The target project’s model and view files
   - `projects/shared/SPEC_CHEATSHEET.md` as a quick orientation aid only

3. **The allowed taxonomy**
   - Valid element kinds, deployment node kinds, tags, and relationship names must be confirmed before creating anything.
   - Naming conventions must be confirmed from the repository itself, especially PascalCase public names such as `Actor_Person`, `System_Existing`, and `Container_Api`.

4. **The modeling scope**
   - Confirm the system boundary and whether you are changing C1 only, C2 only, or eventually drilling into C3.
   - Confirm the target files that will hold the model and the views.

## What happens after that

Once project, taxonomy, naming, and source files are locked in, hand off to the modeling workflow that sequences the work from context to containers to components.

- The framing step’s job is to prevent project mix-ups and taxonomy errors.
- The next step’s job is to orchestrate the actual C1 → C2 → C3 modeling changes in order.

That order matters: first establish project context and repository rules, then sequence the model changes.
