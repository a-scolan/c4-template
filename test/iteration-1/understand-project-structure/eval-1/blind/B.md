## Safe sequence after switching projects before editing a C3 view

1. **Re-identify the active project from the file path and nearest project config.**
   - `projects/template/...` means the template project.
   - `projects/spec-showcase/...` means the showcase project.
   - Do not rely on the previous project still being active after a switch.

2. **Re-read the target project’s config and local files.**
   - Open the target project’s `likec4.config.json`.
   - Re-read the target project’s model file and view file.
   - Confirm the C3 view you want to edit belongs to that same project.

3. **Re-read the shared taxonomy used by both projects.**
   - Both project configs include `../shared`, so re-check `projects/shared/spec-context.c4`, `projects/shared/spec-containers.c4`, `projects/shared/spec-components.c4`, `projects/shared/spec-global.c4`, and `projects/shared/spec-deployment.c4`.
   - Use `projects/shared/SPEC_CHEATSHEET.md` only as a quick recap, not as the final authority.

4. **Refresh the editing assumptions before touching the C3 view.**
   - Confirm the valid element kinds and relationship names.
   - Confirm the parent system and parent container IDs in the target model.
   - Confirm the target C3 view ID, title, includes, and any `navigateTo` links.

5. **Check C3-specific fit.**
   - Make sure the detailed view is attached to the correct container.
   - Make sure the components you want to show either already exist or are planned in the same parent container.
   - Make sure the view does not accidentally reference elements from the other project.

## Risks this avoids

- **Stale project context:** editing with assumptions from the previously opened project.
- **Invalid taxonomy:** using a kind or relationship that is not defined in the shared specs.
- **Wrong C3 parent:** attaching a component view to the wrong container or even the wrong system.
- **Wrong file target:** updating a view file in one project while thinking about the other one.
- **Broken drill-downs:** leaving `navigateTo` links or includes pointing at the wrong elements.
