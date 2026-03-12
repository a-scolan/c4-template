Start with a strict preflight before adding any new API container.

## Preflight

1. **Identify the active project first.**
   - If you are editing files under `projects/template/`, the project is `template-project`.
   - If you are editing files under `projects/spec-showcase/`, the project is `spec-showcase`.
   - Before editing, confirm that with `list-projects`, then run `read-project-summary` for the explicit project id.

2. **Load the project-level source of truth.**
   - Read the project `likec4.config.json` first.
   - In this repository, both known project configs include `../shared`, so shared specs are part of the active taxonomy.
   - Use the config to confirm include paths and image aliases before trusting any model file.

3. **Load the workspace taxonomy from shared specs.**
   - `projects/shared/spec-context.c4` → C1 kinds such as `Actor_Person`, `Actor_Staff`, `Actor_Admin`, `System_New`, `System_Existing`, `System_Legacy`, `System_External`
   - `projects/shared/spec-containers.c4` → C2 kinds such as `Container_Api`, `Container_Webapp`, `Container_Database`, `Container_Queue`, `Container_Browser`, `Container_Spa`, `Container_ApplicationServer`
   - `projects/shared/spec-components.c4` → C3 kind `Component`
   - `projects/shared/spec-global.c4` → model relationships `uses`, `calls`, `async`, `reads`, `writes`
   - `projects/shared/spec-deployment.c4` → deployment-only tags and deployment relationships; do not mix these into a C2 model edit unless you are editing deployment.

4. **Load the quick reference, but treat specs as authoritative.**
   - `projects/shared/SPEC_CHEATSHEET.md` is useful for orientation.
   - The actual `spec-*.c4` files remain the final source of truth if there is any mismatch.

5. **Load the current project structure before changing it.**
   - Read the active model and view files.
   - In `projects/template/`, the current structure is:
     - C1: `user`, `mySystem`, `emailService`
     - C2: `mySystem.webapp`, `mySystem.api`, `mySystem.database`
     - Views currently organized under `views`, `views 'C1'`, and `views 'C2'`
   - Reconfirm this with `read-project-summary` so you do not edit against stale context.

## What is valid here

- **Container kind for the new API:** `Container_Api`
- **Likely related kinds nearby:** `Container_Webapp`, `Container_Database`, `Container_Queue`, `Component`
- **Valid model relationships:** `uses`, `calls`, `async`, `reads`, `writes`
- **Relevant tags already defined by the taxonomy:** `#Container`, `#Api`, `#Database`, `#Queue`, `#Internal`, `#External`

## Ordered C1 → C2 → C3 plan

1. **C1 — confirm boundary and purpose.**
   - Decide whether the new API changes the system boundary or just extends the existing system.
   - Check whether it introduces a new external dependency or actor-facing interaction.

2. **C2 — add the runtime container.**
   - Add a new `Container_Api` under the correct `System_*`.
   - Give it a concrete `technology` and a short responsibility-focused description.
   - Add only valid relationships from the shared taxonomy, for example `calls`, `reads`, `writes`, or `async`.
   - Update the relevant C2 view so the new API appears in the correct container context.

3. **C3 — only if the API needs internal detail.**
   - Create a C3 view only if this API is complex, risky, or central enough to justify components.
   - If needed, model internal `Component` elements and their internal relationships.
   - If the API is straightforward, stop at C2.

4. **Revalidate before further edits.**
   - Re-run `read-project-summary` after the structural change.
   - Confirm the new container kind, relationships, and view placement still match the active project taxonomy.
