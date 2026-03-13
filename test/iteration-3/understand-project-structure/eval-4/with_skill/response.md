If you are coming from UML or ArchiMate, learn this LikeC4 workspace in this order:
1. Shared semantic taxonomy: `projects/shared/SPEC_CHEATSHEET.md` plus the authoritative declarations in `projects/shared/spec-context.c4`, `spec-containers.c4`, `spec-components.c4`, `spec-global.c4`, and `spec-deployment.c4`.
2. Project-specific wiring: the chosen project's `likec4.config.json` and the nearby model/view files under `projects/<project>/`.
3. Workflow guidance: `.github/skills/` explains how to work safely, but it does not redefine the taxonomy.
The real sources of truth here are the shared specs and the project summary for the active project. Concrete taxonomy already used in this repo includes `Actor_Person`, `System_External`, `Container_Api`, `Container_Queue`, `Container_Database`, `Component`, and model relationships `uses`, `calls`, `async`, `reads`, `writes`. Global tags include `#Internal`, `#External`, `#Legacy`, `#Cloud`, `#Saas`, `#Queue`, and `#Security`.
Handoff after preflight:
- use `c4-modeling-process` if you need to sequence modeling from C1 -> C2 -> C3;
- otherwise hand off to a narrower editing skill only after the project, taxonomy, and target files are validated.
That keeps you from importing UML habits into the wrong LikeC4 kind, tag, or parent boundary.
