## How to validate the change from `calls` to `async`

1. Reconfirm the relationship endpoints.
- Identify the exact source and target FQNs for the changed edge.
- Verify both elements still exist at the intended level and that the relationship direction is still correct.
- Make sure the edited edge is the one actually used by the affected C2 views, not a duplicate relationship elsewhere.

2. Validate the meaning of `async`.
- Ask whether the interaction truly became asynchronous, or whether only the label changed.
- If the flow now depends on a queue, topic, broker, worker, or delayed processing step, the model may need an extra element instead of a direct `async` edge.
- Re-check the relationship title, description, and technology so they still describe the real runtime behavior.

3. Inspect every impacted view.
- Re-open each C2 view that contains either endpoint.
- Compare the before and after rendering: odd layout, confusing edge direction, or a misleading label can signal a modeling problem even when syntax is accepted.
- Look for views that now imply a direct real-time exchange when the system actually uses an intermediary.

4. Compare model consistency across views.
- Make sure the same source and target pair is described consistently in focused views and broader container views.
- If one view still looks natural with `calls` but another looks wrong with `async`, the model structure may no longer match the architecture narrative.

5. Run editor validation before commit.
- Ensure the Problems panel stays clean.
- Re-render the affected views after the change.
- Check that no unrelated relationships disappeared or became visually dominant because of the new edge type.

6. Decide whether the model needs a structural change.
- If the diagram looks odd because the interaction is no longer a direct request/response, do not stop at “no syntax error”.
- Model the real mediator or background processor explicitly, then validate the views again.
