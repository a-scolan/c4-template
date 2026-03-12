Do not stop at “LikeC4 no longer complains.” A valid syntax change can still be a bad model change.

1. **Revalidate the model semantics first**
   - Run `read-project-summary` to confirm `async` is a valid relationship kind in the project.
   - Recheck that both containers involved in the change still exist with the correct FQNs.

2. **Inspect the relationship directly**
   - Use `find-relationships` between the two containers and compare the old `calls` edge with the new `async` edge.
   - Verify the direction is still correct, the label still describes the real interaction, the technology value still makes sense, and there is no leftover duplicate `calls` relationship.
   - Confirm you did not accidentally change a request/response interaction into an event-driven one only at the syntax level.

3. **Validate every impacted view, not just the source file**
   - Preview each C2 view that includes either endpoint of the relationship.
   - In this template, if the changed relationship is `mySystem.webapp -> mySystem.api`, inspect both `c2_containers` and `c2_webapp_details`.
   - Compare before/after rendering to see whether the new edge changes layout, emphasis, or the visible story of the system.

4. **Check for side effects in dependent views**
   - If other views inherit or include these elements, compare them as well.
   - An “odd” C2 view often means the relationship kind is technically allowed but semantically wrong for the intended diagram.

5. **Finish with editor and render checks**
   - Review the VS Code Problems panel.
   - Run the local renderer and confirm the diagrams still render cleanly.
   - Only treat the change as correct when both the relationship inventory and the affected views look right before and after the swap.
