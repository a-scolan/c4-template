Short answer: No — `projects/spec-showcase/container-views.c4` is not automatically authoritative for another project.

Validate first:
1. Active target project id
2. Target project's taxonomy via `read-project-summary` (kinds/relationships/tags)
3. Target project's source files via `likec4.config.json` includes
4. Existing valid queue/API patterns inside that same target project

Only reuse showcase patterns if they match the target project's allowed taxonomy and conventions.
