# Validate model correctness after `calls` → `async`

1. **Confirm relationship kind is valid in spec**
   - Verify `async` is an allowed relationship kind in your LikeC4 specification.
   - Ensure there is no fallback behavior that silently reinterprets unsupported kinds.

2. **Re-check semantic intent (not just syntax)**
   - Confirm source/target direction still matches producer/consumer behavior.
   - Validate label/technology/description still describe asynchronous interaction accurately.

3. **Inspect impact on view filtering/styling**
   - Check whether the C2 view includes/excludes relationships by kind and whether `async` changes visibility.
   - Verify style rules (edge style, color, grouping) for `async` are defined and not causing odd rendering.

4. **Compare model-wide consistency**
   - Search for remaining `calls` relationships for the same interaction pattern and align taxonomy.
   - Ensure downstream views/legends still match the updated relationship vocabulary.

5. **Render-level diagnostics**
   - Re-render C2 and inspect edge routing, labels, and overlap.
   - If layout changed unexpectedly, verify node inclusion scope before blaming layout.

6. **Targeted correctness checks**
   - Validate there is exactly one intended relationship between the two containers (or clearly documented multiples).
   - Confirm no duplicate or opposite-direction relationship was introduced during replacement.

7. **Acceptance gate**
   - Model validates cleanly.
   - Relationship semantics are correct and consistent.
   - C2 rendering is understandable and faithful to asynchronous behavior.
