## Focused validation for C2 parent context and include scope

Use a **quick validation** targeted to your C2 detail view.

1. **Parent context rule (C2)**
   - Confirm the view still shows the **parent system boundary** containing `web application` and `API`.
   - If user is external, keep it outside boundary; if internal actor, place correctly by model semantics.

2. **Element inclusion sanity**
   - Verify the three expected participants are present: user, web app, API.
   - Verify no unrelated containers are pulled in unexpectedly.

3. **Include pattern audit**
   - Inspect include rules for broad selectors.
   - Prefer scoped includes (for example by system/container path) over catch-all patterns.
   - Red flag: `include **` in a focused C2 view.

4. **Neighbor/relationship sanity**
   - Ensure only relevant neighbors/edges are present.
   - Confirm relationship kind remains semantic (`calls`/`async`/...) and protocol stays in `technology`.

5. **Render check**
   - Open the view and verify visual intent: parent boundary visible, no noisy extras, readable focus.

## Minimal acceptance criteria

- [ ] parent system boundary is visible in this C2
- [ ] only intended elements are included
- [ ] include scope is narrow (not global/wildcard-heavy)
- [ ] displayed relationships match intended story
