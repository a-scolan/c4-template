## How to validate `c2_webapp_details`

1. Check the parent context first.
- This is a C2 view, so its internal elements should stay inside the `mySystem` container boundary.
- `mySystem.webapp` and `mySystem.api` are both in the right parent context; `user` is the only external actor shown, which is fine.
- If you add more internal elements later, prefer other `mySystem.*` children only when they are truly needed for this story.

2. Keep the includes explicit.
- The current pattern is good because it explicitly includes `user`, `mySystem.webapp`, and `mySystem.api`.
- Avoid broad includes such as `include mySystem.*` or `include mySystem` in this view, because they can silently pull in `database`, future containers, or relationships you did not mean to show.
- Re-scan the view and confirm there is no copied include that widens the scope.

3. Validate the rendered result.
- Re-open the view and confirm it shows only the actor and the two targeted containers.
- Make sure the parent context is still obvious: the view should read as a focused detail of `mySystem`, not a second full container overview.
- Check whether any relationship to `database` or `emailService` appears indirectly; if so, the include pattern is too broad or the view intent is drifting.

4. Check consistency with the higher-level container view.
- Follow the navigation from `c2_containers` to `c2_webapp_details` and confirm the focused view is a narrower slice of the same story.
- `c2_containers` may stay broad, but `c2_webapp_details` should remain selective and intentional.

5. Final editor checks.
- Ensure the Problems panel is clean.
- If you change the include list, re-render immediately and compare before and after to catch accidental scope expansion.
- If another element is needed, add it explicitly by FQN instead of broadening the whole view.
