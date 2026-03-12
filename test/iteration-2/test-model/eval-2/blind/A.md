A clean syntax result only means LikeC4 accepted the DSL. It does **not** prove the relationship is still architecturally correct. For this change, validate the model in four passes.

## 1. Re-check structure and relationship availability

- Run `read-project-summary` first.
- Confirm `async` is a valid declared relationship kind in the project spec.
- Verify both containers still exist with the expected kinds and hierarchy.

## 2. Re-check endpoints and FQNs

- Use `search-element` on both containers.
- Confirm the source and target FQNs are still exactly the ones you intended.
- Make sure the old `calls` edge was actually replaced rather than leaving behind a duplicate or stale reference.

## 3. Compare the relationship **before and after** semantically

- Use `find-relationships` between the two containers.
- Check whether only the relationship kind changed, or whether label, direction, technology, or multiplicity assumptions changed too.
- Validate that `async` is semantically appropriate for a structural C2 relationship, not merely accepted by the parser.
- If the interaction is really about timing or message flow rather than static dependency, consider whether the important detail belongs in a dynamic/sequence view instead.

## 4. Validate all impacted views, not just the model file

- Preview the affected C2 view with `open-view`.
- Also inspect any other views that include either container or that relationship path.
- Compare the rendered result **before vs. after** if you can: edge label, direction, unexpected routing, missing context, or layout drift.
- If the C2 view now looks odd, check whether the new relationship kind changed what the view communicates even though the syntax is valid.

## Final pre-commit checks

- Check the VS Code Problems panel for hidden compile issues or warnings.
- Run local rendering (`likec4 start`) so the diagrams are exercised end to end.
- If rendering is clean but the diagram still looks misleading, treat it as a modeling problem, not a syntax success.

## Short verdict rule

If `async` is valid, the FQNs resolve, the relationship is semantically right, and the affected C2 views still communicate the intended architecture, then the change is truly correct. If any one of those fails, the model is only *syntactically acceptable*—and that is a sneaky class of wrong.