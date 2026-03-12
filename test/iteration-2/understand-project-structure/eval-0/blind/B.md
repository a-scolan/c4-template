## Preflight checklist

### 1. Lock the active project first
- Do **not** assume the active project in this repository.
- Identify it from the `likec4.config.json` next to the files you intend to edit:
  - `projects/template/likec4.config.json` → project name `template-project`
  - `projects/spec-showcase/likec4.config.json` → project name `spec-showcase`
- Both visible projects include `../shared`, so they inherit the shared taxonomy from `projects/shared/`.

### 2. Confirm the source-of-truth inputs
- **Project config:** the selected project's `likec4.config.json`
- **Shared taxonomy:**
  - `projects/shared/spec-context.c4`
  - `projects/shared/spec-containers.c4`
  - `projects/shared/spec-components.c4`
  - `projects/shared/spec-global.c4`
  - `projects/shared/spec-deployment.c4` (only if deployment is involved)
- **Quick reference:** `projects/shared/SPEC_CHEATSHEET.md`
- **Current assembled project context:** rerun the project summary for the selected project if that tooling is available; otherwise derive the same context from the selected project's model/view files.
- **Project-local source files:**
  - `projects/template/system-model.c4`, `projects/template/system-views.c4`
  - or, for the showcase project, files such as `projects/spec-showcase/components.c4` and `projects/spec-showcase/component-views.c4`

### 3. Validate the taxonomy you can actually use
- **C1 kinds:** `Actor_Person`, `Actor_Staff`, `Actor_Admin`, `System_New`, `System_Existing`, `System_Legacy`, `System_External`
- **C2 kinds relevant to an API addition:** `Container_Api`, `Container_Webapp`, `Container_Database`, `Container_Queue`, `Container_Browser`, `Container_Spa`, `Container_WebServer`, `Container_ApplicationServer`
- **C3 kind:** `Component`
- **Valid model relationships:** `uses`, `calls`, `async`, `reads`, `writes`
- **Common tags available in this workspace:** `#Container`, `#Api`, `#Component`, `#Internal`, `#External`, `#Legacy`, `#Cloud`, `#Saas`, `#Queue`, `#Security`

### 4. Ordered C1 → C2 → C3 plan before modification
1. **C1 - confirm the system boundary**
   - Identify the parent system that will own the new API container.
   - Confirm whether the API changes any actor or external-system relationships at context level.
   - If the API is internal-only, C1 may stay unchanged; if it introduces a new external dependency, update C1 intentionally.

2. **C2 - add the new API container**
   - Add the container as `Container_Api` under the correct system in the project model file.
   - Connect it with only valid model relationships (`calls`, `reads`, `writes`, `async`, `uses`) and attach the interaction technology to each relationship.
   - Update or create the relevant container view so the new API is visible in the right C2 diagram.

3. **C3 - add internal API detail only if needed**
   - If the new API needs internal structure, add `Component` children inside that API container.
   - Create or update the C3 view so it is explicitly scoped to the new API container, not to the whole system.
   - Recheck that the C3 view parent matches the exact container you added in C2.

### Bottom line
The safe order is: **pick the project → confirm shared taxonomy and project-local files → verify the parent system → add `Container_Api` at C2 → only then break it down into C3 components if required**.
