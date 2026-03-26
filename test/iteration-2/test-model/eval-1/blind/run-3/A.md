## How to validate C2 parent context and include precision

Use a targeted quick pass:

1. **Parent boundary**
   - Confirm your C2 still includes the parent system boundary.

2. **Focused participants**
   - Confirm user + web app + API are present as intended.
   - Confirm no accidental extra containers appear.

3. **Include precision**
   - Review include selectors.
   - Replace broad wildcard patterns with scoped selectors when possible.

4. **Relationship clarity**
   - Ensure displayed relationships match your scenario and are not noisy.

5. **Render sanity**
   - Re-open the view and verify boundary/context readability.

## Pass criteria

- [ ] parent context is visible
- [ ] include scope is focused
- [ ] only intended elements/edges are shown
