To validate `c2_webapp_details`, check both **parent context** and **include scope**:

1. **Keep the parent context explicit**
   - Because this is a C2 view, validate that the `mySystem` boundary is still clearly present around `mySystem.webapp` and `mySystem.api`.
   - The containers should not appear as floating elements without their surrounding system context.
   - For the detailed parent-context rules and view-structure guidance, hand off to the `design-view` skill.

2. **Audit the include statements**
   - In this view, explicit includes are the safest option: `user`, `mySystem.webapp`, and `mySystem.api`.
   - Avoid broad patterns such as `include **`.
   - Be careful with `include mySystem.*` here, because it could pull in `mySystem.database` or future containers that do not belong in this focused detail view.

3. **Preview the actual rendering**
   - Open the rendered `c2_webapp_details` view and confirm it shows only the intended elements.
   - Make sure no unexpected neighbor such as `emailService` or `mySystem.database` appears due to an over-broad include.
   - Verify the rank hints still match the visual flow: `user` as source and `mySystem.api` as sink.

4. **Finish with integrity checks**
   - Check the VS Code Problems panel for reference or syntax issues.
   - Run the local renderer to confirm the view still compiles and displays correctly.

If the rendering is correct, the parent boundary is explicit, and the includes stay narrow, the view is preserving the right C2 context.
