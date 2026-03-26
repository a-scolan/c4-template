## Full validation plan (pre-commit)

Because you added a **new container** and a **new C2 view**, use a **full validation** pass (not only syntax).

1. **Project/taxonomy check**
   - Confirm container kind is valid in shared specs.
   - Confirm relationship kinds allowed for the project (`calls`, `async`, `reads`, `writes`, `uses`).

2. **Reference integrity (FQNs)**
   - Verify the new worker FQN resolves exactly where expected (system/container hierarchy).
   - Verify all references in views point to existing elements.
   - If deployment was touched, verify every `instanceOf` target is a real model container.

3. **Relationship correctness**
   - Validate each new/changed edge has a valid kind and meaningful label.
   - Keep transport/protocol in `technology` (not as relationship kind).
   - Ensure application traffic is modeled in logical model (not duplicated in deployment just to "make diagrams look right").

4. **C2 rendering and scope**
   - Ensure the C2 view includes the **parent system boundary**.
   - Ensure expected neighbors appear (and only relevant ones).
   - Check include patterns are scoped (avoid over-broad patterns like `**` unless intentional).

5. **Risk-focused visual checks**
   - Worker appears in the intended boundary.
   - New edges direction and labels match the use case.
   - No accidental extra nodes from broad include.

6. **Problems panel + final gate**
   - Confirm no unresolved references, kind errors, or relationship type issues.
   - If all checks pass, commit with confidence.

## Quick pass/fail checklist

- [ ] kinds valid
- [ ] FQNs resolve
- [ ] relationship kinds/labels correct
- [ ] protocol in `technology`
- [ ] C2 keeps parent context
- [ ] include scope is not over-broad
- [ ] view renders as expected
- [ ] editor reports no model errors
