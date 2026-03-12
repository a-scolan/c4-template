## What to understand first in this workspace
If you are coming from UML or ArchiMate, the safest approach is to learn the **repository-local LikeC4 taxonomy and file layout first**, rather than importing outside naming conventions.

### 1. Local workspace conventions
- This is a **multi-project** LikeC4 workspace, so choose the target project before editing.
- Each project has its own `likec4.config.json`.
- Shared taxonomy lives under `projects/shared/` and is inherited by projects through their config includes.
- Project-specific model and view files live inside each project folder, for example:
  - `projects/template/`
  - `projects/spec-showcase/`
- `.github/skills/` is part of the local workflow scaffolding, but it is **not** the semantic source of truth for kinds or relationships.

### 2. Real sources of truth
Use these in this order:
1. **Quick orientation:** `projects/shared/SPEC_CHEATSHEET.md`
2. **Actual taxonomy definitions:**
   - `projects/shared/spec-context.c4`
   - `projects/shared/spec-containers.c4`
   - `projects/shared/spec-components.c4`
   - `projects/shared/spec-global.c4`
   - `projects/shared/spec-deployment.c4`
3. **Active project configuration:** the selected project's `likec4.config.json`
4. **Active project model/view files:** for example `projects/template/system-model.c4`, `projects/template/system-views.c4`, `projects/spec-showcase/components.c4`, `projects/spec-showcase/component-views.c4`
5. **Project summary:** use it as the assembled view of the selected project when available

### 3. Taxonomy examples actually used here
- **Kinds:** `System_Existing`, `System_External`, `Container_Api`, `Container_Webapp`, `Container_Database`, `Component`
- **Model relationships:** `uses`, `calls`, `async`, `reads`, `writes`
- **Tags:** `#Container`, `#Api`, `#Component`, `#Internal`, `#External`, `#Cloud`, `#Queue`, `#Security`

### 4. Practical modeling rule
Map your intent into the taxonomy that already exists here.
- If you want an application service at C2, use `Container_Api`, not a UML stereotype or a new custom name.
- If you need internal structure at C3, use `Component` inside the owning container.
- If you need interactions, stay within the valid relationship set already defined in shared specs.

## What to hand off to next
After that workspace preflight, hand off to **`c4-modeling-process`** so the actual modeling work can be sequenced correctly from **C1 → C2 → C3** without breaking repository conventions.
