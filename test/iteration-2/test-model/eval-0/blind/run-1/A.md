# LikeC4 validation plan (pre-commit)

1. **Validate element kinds and hierarchy**
   - Confirm `worker` is declared with the intended kind (e.g., container) in the main model file.
   - Verify parent nesting is correct (no accidental move under a wrong system/container).
   - Check naming consistency with existing C1/C2 structure.

2. **Validate FQNs and uniqueness**
   - Confirm the worker FQN follows current naming conventions and parent path.
   - Ensure there is no duplicate id/title collision with existing elements.
   - Verify all references in views point to the same canonical element FQN.

3. **Validate relationships semantics**
   - Confirm each new/updated relationship involving `worker` uses an allowed relationship kind.
   - Check directionality (source/target) matches runtime/data flow intent.
   - Verify relationship labels/technologies are still meaningful and consistent.

4. **Validate dedicated C2 view scoping**
   - Ensure the new C2 view anchors on the expected parent container/system.
   - Confirm includes are minimal (only required elements) and do not pull unrelated siblings.
   - Check that relationship visibility in the view reflects intended scope.

5. **Render and inspect diagram quality**
   - Render the model and inspect layout for orphan nodes, hidden edges, or over-clutter.
   - Confirm the worker appears exactly once in the expected place.
   - Check edge labels and direction arrows are readable and not ambiguous.

6. **Cross-view consistency checks**
   - Compare C2 with adjacent C1/C3 views to ensure no contradictory modeling.
   - Verify shared elements keep identical FQNs and relationship meaning across views.

7. **Regression and commit gate**
   - Run model validation/linting and ensure zero warnings relevant to worker/view.
   - Re-render once after any include/filter adjustments.
   - Commit only when model validity, view scope, and readability all pass.
