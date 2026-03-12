Validate the **parent context first**: a C2 view should not show only `user`, `web application`, and `API` as floating elements. It should explicitly keep the **parent system boundary** so the containers are shown *within* their system.

## What to check

1. **Parent context is explicit**
   - Confirm the parent system is included in the view, not just its children.
   - The web app and API should render inside that system boundary.
   - The user may sit outside the boundary, but the system must still be visible.

2. **Include patterns are scoped, not broad**
   - Review the include rules and prefer targeted includes for the system and the exact containers you want.
   - Be suspicious of patterns like `include **` or other wildcards that can silently pull in extra neighbors.
   - If you need neighbors, include them intentionally rather than relying on a broad catch-all.

3. **Render the real view**
   - Preview it with `open-view`.
   - Check whether the rendered result contains only the intended set: parent system, user, web application, API, and any explicitly desired neighbors.
   - If unexpected elements appear, the include rules are probably too broad.

4. **Check for hidden problems**
   - Look at the VS Code Problems panel for compile issues.
   - If the view renders but still feels wrong, compare the rendered boundary and included elements against the intended C2 scope.

## Important handoff

For the **detailed rules about how a view should keep parent context and how to structure includes**, defer to the `design-view` skill. That is the right place for the deeper design guidance; here, the goal is to validate that the view still respects those rules and actually renders as intended.

## Practical rule of thumb

- **Good:** parent system explicitly included, containers shown inside it, neighbors added deliberately
- **Bad:** isolated containers with no system boundary, or broad include patterns that drag half the model into the view
