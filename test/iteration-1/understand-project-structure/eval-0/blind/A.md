## Preflight before adding a new API container

1. **Identify the active project first.**
   - If the file you will edit is under `projects/template/`, the active project is the one configured by `projects/template/likec4.config.json` (`template-project`).
   - If it is under `projects/spec-showcase/`, the active project is the one configured by `projects/spec-showcase/likec4.config.json` (`spec-showcase`).
   - If no file is open yet, choose the target project folder before making any model change.

2. **Read the real sources of truth in this order.**
   - Project config: the target project’s `likec4.config.json`
   - Shared taxonomy: `projects/shared/spec-context.c4`, `projects/shared/spec-containers.c4`, `projects/shared/spec-components.c4`, `projects/shared/spec-global.c4`, `projects/shared/spec-deployment.c4`
   - Quick reference: `projects/shared/SPEC_CHEATSHEET.md` for orientation only
   - Project model and views: the target project’s model file and view file (for example `projects/template/system-model.c4` and `projects/template/system-views.c4`)

3. **Confirm the valid taxonomy before editing.**
   - C1 kinds: `Actor_Person`, `Actor_Staff`, `Actor_Admin`, `System_New`, `System_Existing`, `System_Legacy`, `System_External`
   - C2 kinds include `Container_Api`, `Container_Webapp`, `Container_Database`, `Container_Queue`, `Container_Browser`, `Container_Spa`, `Container_ObjectStorage`, and others defined in `projects/shared/spec-containers.c4`
   - C3 kind: `Component`
   - Model relationships: `uses`, `calls`, `async`, `reads`, `writes`
   - Shared tags relevant to model work include `#Container`, `#Api`, `#Internal`, `#External`, `#Legacy`, `#Cloud`, `#Saas`, `#Queue`, `#Security`

4. **Locate the current system boundary.**
   - Find the owning system in the target model file.
   - Verify whether the new API belongs inside an existing system or requires a C1 change first.
   - Check whether an existing container already fills the same responsibility.

5. **Check the existing view structure before adding anything.**
   - Confirm the current C1, C2, and any detailed views already present.
   - Note current `navigateTo` links so the new API can be exposed consistently.

## Ordered C1 → C2 → C3 plan

1. **C1: lock the context.**
   - Confirm the user, main system, and external systems.
   - Add or adjust context relationships only if the new API changes the system boundary.

2. **C2: add the API container.**
   - Add the new container under the correct system using `Container_Api`.
   - Set `technology` and `description`.
   - Add only valid relationships such as `calls`, `reads`, `writes`, or `async`.
   - Update the container view so the API appears in the right place.

3. **C3: detail the API internals only after C2 is stable.**
   - Create or update a detailed view for the API’s internal parts using `Component`.
   - Keep the C3 parent tied to the correct container.
   - Add drill-down links only after the C2 structure is correct.

4. **Final verification.**
   - Recheck the chosen project, the shared taxonomy, and the target files one last time before saving additional edits.
