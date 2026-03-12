## Safe sequence after switching projects

1. **Revalidate the active project immediately**
   - Rerun `list-projects` and explicitly select the target project.
   - Do not rely on the previously open files or the previous model state.

2. **Refresh the assembled context for the new project**
   - Rerun `read-project-summary` for the selected project.
   - Confirm the project name, included sources, available kinds, relationships, tags, and existing views before touching any C3 file.

3. **Recheck the project-local configuration**
   - Open the target project's `likec4.config.json`.
   - Verify its include paths and confirm which shared specs it inherits.
   - In this workspace, both visible projects include `../shared`, but that still needs to be revalidated after a switch.

4. **Reread the shared taxonomy before C3 edits**
   - Recheck `projects/shared/SPEC_CHEATSHEET.md` for the quick map.
   - Recheck the real definitions in:
     - `projects/shared/spec-components.c4`
     - `projects/shared/spec-containers.c4`
     - `projects/shared/spec-global.c4`
   - This avoids carrying over assumptions from the previous project.

5. **Reconfirm the C3 parent and the owning files**
   - Identify the exact container that owns the component view.
   - Reopen the project model/view files that define that parent container and its views.
   - For example, `projects/spec-showcase/component-views.c4` defines `view api_components of api_container`, so the C3 view is tied to `api_container`, not to an arbitrary API in another project.

6. **Only then edit the C3 view**
   - Make sure the container name in the C3 view still exists in the selected project.
   - Confirm the included elements are valid `Component` children of that container.

## MCP checks to rerun after a project switch
- `list-projects`
- `read-project-summary`
- If needed, follow with element-level checks for the target container/view after the project has been reselected

## Risks this avoids
- **Stale context:** editing with the previous project's taxonomy, elements, or views still in mind
- **Invalid kind/relationship use:** reusing a token that is not valid for the selected project's current spec set
- **Wrong C3 parent:** attaching the view to the wrong container, or to a container name that exists only in another project
- **Wrong file edits:** modifying the wrong project's model/view files because the workspace is multi-project
