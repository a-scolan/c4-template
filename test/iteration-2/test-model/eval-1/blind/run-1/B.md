# Validate C2 context and include scope

1. **Confirm the C2 anchor is correct**
   - Verify the C2 view is scoped to the intended parent (typically the software system or target container boundary).
   - Ensure `user`, `web application`, and `API` are included as members of the expected context, not from a different parent branch.

2. **Check parent-context integrity**
   - For each shown element, confirm its FQN path resolves under the intended hierarchy.
   - Ensure no element is being represented through an unintended alias or duplicated declaration.

3. **Audit include statements for breadth**
   - Replace broad selectors with explicit includes where possible.
   - Validate that includes do not accidentally pull siblings/descendants not needed for this C2 purpose.
   - Confirm exclusion rules are not masking a too-broad include.

4. **Relationship scope validation**
   - Check only relevant interactions among user/web app/API are visible.
   - Ensure no cross-boundary relationship appears unless intentionally part of the scenario.

5. **Render verification**
   - Render the C2 view and inspect for extra nodes/edges that indicate over-broad include logic.
   - Confirm the visible boundary matches the intended parent context narrative.

6. **Regression checks against adjacent views**
   - Compare with neighboring context/container views to ensure consistent containment and naming.
   - Confirm C2 remains focused detail, not a partial context dump.

7. **Pass criteria before commit**
   - Parent context is unambiguous.
   - Includes are minimal and intentional.
   - Diagram shows only required elements and relationships for this detail view.
