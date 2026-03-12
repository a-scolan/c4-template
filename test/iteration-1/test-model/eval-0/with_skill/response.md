For the `mySystem.worker` change in `projects/template/system-model.c4` and `projects/template/system-views.c4`, use this pre-commit validation plan:

1. **Validate structure and kinds first**
   - Run `read-project-summary` for the template project.
   - Confirm the container kind used for `mySystem.worker` is declared in the shared spec files.
   - Check that any tags or metadata used by the new container are valid and that no orphaned elements were introduced.

2. **Verify references and FQNs**
   - Use `search-element` for `mySystem`, `mySystem.worker`, and any nested references used in views.
   - Confirm the new dedicated C2 view points at the correct FQN and that any `navigateTo` target resolves.
   - Make sure the container is still nested under `mySystem`, not accidentally modeled as a sibling system.

3. **Validate relationships semantically**
   - Use `find-relationships` between `mySystem.worker` and every element it connects to, especially `mySystem.api`, `mySystem.database`, `mySystem.webapp`, or `emailService` if applicable.
   - Check that each relationship uses a valid typed kind, keeps the correct direction, has a descriptive label, and does not duplicate an existing edge.
   - Verify there are no leftover reverse/return relationships that should not exist.

4. **Validate rendering and view scope**
   - Preview the new dedicated C2 view and the broader `c2_containers` view.
   - Confirm `mySystem.worker` renders inside the `mySystem` boundary and that the view includes are scoped tightly enough to avoid unrelated elements leaking in.
   - Recheck rank hints if the new worker changes the layout flow.

5. **Do final editor and renderer checks**
   - Review the VS Code Problems panel for compile or reference errors.
   - Run `likec4 start` locally and confirm the diagrams render cleanly.
   - Before commit, compare the affected views once more to ensure the worker appears only where intended.
