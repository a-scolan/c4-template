## Quick C2 validation for context + include scope

For this case, a **quick validation** is enough.

1. **Parent context first**
   - Ensure the C2 view still shows the containing system boundary.
   - Ensure actor placement (inside/outside boundary) matches your model semantics.

2. **Expected participants only**
   - Confirm user, web app, and API are all present.
   - Confirm no unrelated container appears accidentally.

3. **Check include rules for blast radius**
   - Review include selectors for broad wildcards.
   - Prefer narrow patterns targeting the intended system/container scope.

4. **Check edge intent**
   - Ensure shown relationships are exactly the intended interactions.
   - Relationship kind should remain semantic, protocol stays in `technology`.

5. **Visual verification**
   - Re-open the view and confirm: clear focus, correct boundary, no noisy extras.

## Acceptance checklist

- [ ] parent system boundary is visible
- [ ] only intended elements are included
- [ ] include rules are scoped and controlled
- [ ] relationships shown are intentional and readable
