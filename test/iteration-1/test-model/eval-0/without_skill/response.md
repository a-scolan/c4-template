## Validation plan

1. Confirm the new container is modeled at the right level.
- In `projects/template/system-model.c4`, make sure `worker` is declared inside `mySystem`, alongside `webapp`, `api`, and `database`.
- Verify it uses a container kind that matches its role, not a system or component kind.
- Check that its name, title, technology, and description are consistent with the rest of the container layer.

2. Verify the new FQN and every reference to it.
- Confirm the full identifier is `mySystem.worker`.
- Search for every `worker` reference in the model and views; there should be no orphaned `worker`, mistyped FQNs, or stale old names.
- If the dedicated C2 view or any navigation points to the new container, verify the view id is unique and each reference matches the final FQN exactly.

3. Re-check relationships semantically, not just syntactically.
- Inspect every incoming and outgoing relationship attached to `mySystem.worker`.
- Make sure each source and target lives at the intended abstraction level and that the direction is correct.
- Confirm labels, descriptions, and technologies still describe the real interaction model.
- Watch for duplicate or contradictory edges if `worker` overlaps with existing `api` or `database` responsibilities.

4. Validate the affected views.
- Open the main container view and the new dedicated C2 view.
- Check that `worker` appears in the expected parent context under `mySystem`.
- Make sure only the intended neighboring elements are included in the dedicated view; avoid pulling in unrelated containers unless they are needed to explain the interaction.
- Verify edge routing, labels, and layout still read clearly after the change.

5. Run editor validation before commit.
- Ensure the Problems panel is clean.
- Re-render the views after each edit, not only the full model.
- Compare the dedicated C2 view with the main container view to confirm the new container is represented consistently in both.

6. Do a final sanity check.
- Confirm `c1_context` still stays at system level and does not accidentally expose the new container.
- Confirm `c2_containers` and the new dedicated C2 view tell the same story about `worker`.
- If the new behavior depends on a queue, broker, or scheduled trigger, consider whether that infrastructure also needs to be modeled instead of leaving `worker` as an isolated box.
