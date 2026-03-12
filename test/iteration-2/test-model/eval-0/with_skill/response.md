Start with **structure and kinds**, not with rendering.

1. **Validate project structure and declared kinds**
   - Run `read-project-summary` first.
   - Confirm the new `worker` container uses a kind that is actually declared in the shared spec files.
   - Check that any tags, relationship kinds, and deployment kinds touched by this change are also declared.
   - Verify the worker sits under the correct parent system/container hierarchy and is not orphaned.

2. **Validate element references and FQNs**
   - Use `search-element` to confirm the exact FQN of the new worker container.
   - Check every place that references it: model relationships, view includes, exclusions, and any deployment `instanceOf` references.
   - If the worker is nested, verify the full FQN is used consistently in views and relationships.

3. **Validate relationships semantically, not just syntactically**
   - Use `find-relationships` on the worker and each container it connects to.
   - Confirm each relationship kind is valid, direction is correct, labels are descriptive, and technology is in the right field.
   - Check for duplicate links, stale old links, or reverse/return relationships that should not exist.

4. **Validate the dedicated C2 view context**
   - Make sure the view explicitly includes its parent system boundary.
   - Confirm the worker appears **within** that system, alongside the intended peer containers.
   - Check that neighboring containers are included intentionally rather than by accident.
   - Review include patterns and avoid over-broad wildcards such as `include **` unless there is a very strong reason.

5. **Validate actual rendering**
   - Preview the new C2 view with `open-view`.
   - Confirm the expected nodes appear: actor(s), system boundary, existing containers, and the new worker.
   - Look for unexpected elements pulled in by broad includes, missing parents, or brittle rank/layout hints.

6. **Do a final pre-commit sanity pass**
   - Check the VS Code Problems panel for compile errors or warnings.
   - Run local rendering (`likec4 start`) to confirm the diagrams still render cleanly.
   - If anything looks off, fix the model first, then re-open the impacted views.

## Quick pre-commit checklist

- [ ] `read-project-summary` confirms the worker kind and all related kinds are declared
- [ ] `search-element` confirms the worker FQN and all references resolve
- [ ] `find-relationships` confirms valid typed relationships, labels, and direction
- [ ] The C2 view includes the parent system boundary explicitly
- [ ] `open-view` shows only the intended elements
- [ ] VS Code Problems panel is clean
- [ ] Local render succeeds before commit
