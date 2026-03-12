Before editing anything, I would run this preflight.

## Active project

- This repository is multi-project: `projects/template/` and `projects/spec-showcase/` both define a `likec4.config.json`.
- If the change is for the starter project, the active project is `projects/template/`; its config name is `template-project`.
- Reliable identification sequence:
  1. Identify the project folder that contains the model/view you plan to edit.
  2. Read that project's `likec4.config.json`.
  3. Re-run `list-projects` and `read-project-summary` for that project before changing anything.

## Source-of-truth inputs

- Project config:
  - `projects/template/likec4.config.json`
  - `projects/spec-showcase/likec4.config.json`
- Shared specifications:
  - `projects/shared/spec-context.c4`
  - `projects/shared/spec-containers.c4`
  - `projects/shared/spec-components.c4`
  - `projects/shared/spec-global.c4`
  - `projects/shared/spec-deployment.c4` when deployment tags or deployment relationships matter
- Local quick reference:
  - `projects/shared/SPEC_CHEATSHEET.md`
- Current project model/views:
  - `projects/template/system-model.c4`
  - `projects/template/system-views.c4`
- Project inventory / validation source:
  - `read-project-summary` for the active project

## Valid taxonomy already present in this workspace

- C1 kinds: `Actor_Person`, `Actor_Staff`, `Actor_Admin`, `System_New`, `System_Existing`, `System_Legacy`, `System_External`
- C2 kinds include: `Container_Api`, `Container_Webapp`, `Container_Database`, `Container_Queue`, `Container_WebServer`, `Container_IamServer`, `Container_Loadbalancer`
- C3 kind: `Component`
- Model relationships: `uses`, `calls`, `async`, `reads`, `writes`
- Tags already defined here include `#Container`, `#Api`, `#Webapp`, `#Database`, `#Queue`, `#Internal`, `#External`, `#Cloud`, `#Security`

## Ordered C1 → C2 → C3 plan

1. **C1 first** — confirm the system boundary and decide whether the new API belongs inside an existing `System_*` or should instead be modeled as an external system.
2. **C2 next** — add the new runtime boundary as `Container_Api` under the correct system in `system-model.c4`, then connect it only with valid model relationships such as `calls`, `reads`, `writes`, `async`, or `uses`.
3. **Update views** — update the relevant C2 view in `system-views.c4` so the new API is visible in the container landscape.
4. **C3 only if justified** — if the API is architecturally central or internally complex, create a C3 view and model internal `Component` elements inside that API container. If it is simple, stop at C2.
5. **Re-validate** — re-run `read-project-summary` after the change to confirm the project still resolves cleanly.
