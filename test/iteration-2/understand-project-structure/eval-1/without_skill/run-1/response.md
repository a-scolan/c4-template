To avoid context errors after switching projects before editing a C3 view:

- Re-establish active project:
  - `list-projects`
  - choose exact target project id
- Re-load project taxonomy and scope:
  - `read-project-summary` (kinds, relationships, tags, sources)
- Re-locate target container/components in the new project:
  - `search-element` by id/title
  - `read-element` for intended container and key components
- Re-open the exact view context:
  - `read-view` for target C3 view id

MCP checks to re-run before editing:
1. Project identity (correct project id)
2. Allowed element/relationship kinds in that project
3. Element existence in that project namespace
4. Relationship validity between chosen elements
5. View id exists in that project and contains expected nodes

If any check fails, stop edits and fix project selection or taxonomy alignment first.
