## Validating `async` correctness (not just syntax)

Passing syntax is necessary, but not sufficient. Validate semantics and view behavior.

1. **Interaction semantics**
   - Confirm this flow is truly asynchronous (event/message style), not request/response.
   - Do not add a fake return edge to preserve old sync visuals.

2. **Reference and direction checks**
   - Verify source/target FQNs are still correct.
   - Verify direction of the async edge matches producer/consumer reality.
   - Update the edge label to reflect async intent.

3. **C2 context checks**
   - Ensure parent system boundary remains visible.
   - Ensure the async relation remains understandable within the selected neighbors.

4. **Include-scope checks**
   - If the view looks odd, inspect include patterns for over-selection.
   - Tighten includes and re-check readability.

5. **Final validation gate**
   - Confirm no diagnostics and no contradictory modeling choices.

## Success criteria

- [ ] async is domain-correct
- [ ] direction and label reflect actual behavior
- [ ] no synthetic sync-return path added
- [ ] C2 keeps parent context and clear scope
- [ ] view is semantically clean and visually coherent
