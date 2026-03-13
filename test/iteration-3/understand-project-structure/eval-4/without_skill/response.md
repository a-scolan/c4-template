If you are coming from UML or ArchiMate, understand the local conventions before mapping your concepts directly:
- kinds and tags are centrally declared in `projects/shared/spec-*.c4`; this repo is taxonomy-driven, not free-form stereotype-driven
- public names are exact PascalCase (`Container_Api`, `System_Existing`, `Node_Vm`, etc.)
- containers belong inside systems, and components belong inside containers
- technology is carried on the relationship in the system model (`calls`, `reads`, `writes`, `async`, etc.)
- deployment taxonomy is separate from the main model taxonomy
- views do not define taxonomy; they visualize model content

Real sources of truth are:
1. the active project's `likec4.config.json`
2. `projects/shared/spec-context.c4`, `spec-containers.c4`, `spec-components.c4`, `spec-global.c4`, `spec-deployment.c4`
3. the active project's own model/view files

What is not the final authority: `projects/spec-showcase/` and `projects/template/` as examples, plus `projects/shared/SPEC_CHEATSHEET.md` as a quick reference. Useful? Yes. Authoritative? No.

Best next handoff: `lookup-element-kinds`. That is the clean bridge from UML/ArchiMate concepts into this repository's exact LikeC4 taxonomy before you create or edit anything. After that, `create-element` becomes the practical next move.
