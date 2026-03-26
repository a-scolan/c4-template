## Validate async change at model-quality level

To ensure this is truly correct (not merely parseable):

1. **Semantic intent**
   - Confirm this interaction is genuinely async in domain behavior.

2. **Edge correctness**
   - Re-check FQNs, direction, and edge label after changing to `async`.

3. **No fake sync artifacts**
   - Avoid synthetic return-path modeling that contradicts async behavior.

4. **View integrity**
   - Ensure C2 keeps parent context and clear participant scope.
   - If the view looks odd, tighten include scope and re-check.

5. **Final quality gate**
   - Validate no diagnostics and that visual story matches runtime reality.

## Done when

- [ ] async meaning is correct
- [ ] direction/label are coherent
- [ ] no contradictory sync-style artifacts
- [ ] C2 remains clear and context-complete
