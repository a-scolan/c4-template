To avoid context errors after switching projects, re-establish all three boundaries: project config, local model IDs, and local view file.
- Pick the active project's `likec4.config.json` again (`projects/template` or `projects/spec-showcase`).
- Edit only that project's component model and C3 view files; do not point a view in one project at a container declared in the other project.
- Reconfirm that the target container exists in the active project model and actually contains `Component` elements.

The showcase C3 example demonstrates the dependency clearly: `projects/spec-showcase/components.c4` defines `api_container = Container_Api ...` with nested `Component`s, and `projects/spec-showcase/component-views.c4` has `view api_components of api_container`. If `api_container` were missing or from another project, the C3 view would be context-wrong.

If you were back in a tool-enabled workflow, the checks to rerun before editing are the ones that answer: (1) which project is active now, (2) where the target container/view ID is defined, (3) which shared taxonomy is included, and (4) what the current C3 view scope is. In this baseline, the safe equivalent is to re-read the active `likec4.config.json`, the active project's component model file, the active project's C3 view file, and the relevant shared spec file before touching the view.
