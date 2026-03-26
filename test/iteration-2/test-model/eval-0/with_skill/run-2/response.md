## Full validation plan (pre-commit)

Since you introduced a **new worker container** and a **new C2 view**, run a **full validation** before committing.

1. **Validate taxonomy and kinds**
   - Confirm container/relationship kinds are declared by shared specs.
   - Confirm only valid relationship kinds are used (`calls`, `async`, `reads`, `writes`, `uses`).

2. **Validate references and FQNs**
   - Check the worker container FQN resolves in the intended hierarchy.
   - Check all view references resolve to existing elements.
   - If deployment artifacts changed, validate each `instanceOf` target exists.

3. **Validate relationships semantically**
   - Verify kind, direction, and label of each changed edge.
   - Keep protocol data in `technology` instead of turning protocol into relationship kind.
   - Avoid modeling normal app traffic only in deployment.

4. **Validate C2 rendering quality**
   - Parent system boundary must remain visible.
   - Expected neighbors should appear; unrelated nodes should not.
   - Include rules should be focused (avoid broad wildcard scope).

5. **Validate final editor state**
   - No unresolved symbols, unknown kinds, or relationship issues in diagnostics.

## Commit-ready checklist

- [ ] kinds valid
- [ ] FQNs resolve
- [ ] relationships are typed and labeled correctly
- [ ] protocol in `technology`
- [ ] parent system context visible in C2
- [ ] include scope is intentional
- [ ] no model/view errors remain
