## Validate `calls -> async` beyond syntax

Great that syntax passes—now validate semantic correctness and view intent.

1. **Relationship semantics check**
   - Confirm `async` is actually the intended interaction (fire-and-forget/event-driven), not request/response.
   - Ensure no fake return path is implied just to mimic sync behavior.

2. **Model-level consistency**
   - Re-check source/target FQNs and relationship direction.
   - Confirm edge label still describes behavior correctly after switching to async.
   - Keep protocol details in `technology`, not in relationship kind.

3. **C2 storytelling check**
   - In C2, verify async flow remains understandable: initiator, receiver, and expected neighbors.
   - Confirm parent system context is visible.

4. **Why the view may look odd (common causes)**
   - Old sync-oriented wording/labels still present.
   - Extra edges from broad includes cluttering the diagram.
   - Direction now semantically correct but visually surprising due to layout assumptions.

5. **Targeted fix loop**
   - Tighten include scope.
   - Update edge label/description to async intent.
   - Re-open impacted view and confirm readability.

## Done criteria

- [ ] async meaning is domain-correct
- [ ] no synthetic return flow added
- [ ] edge direction + label are coherent
- [ ] C2 keeps parent context and clear focus
- [ ] diagram is semantically and visually consistent
