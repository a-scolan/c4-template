## How to validate it

1. **Keep the parent context explicit**
   - In a C2 detail view, the user should still relate to the same parent system as the web application and the API.
   - Confirm both application elements are siblings under the same system, for example `mySystem.webapp` and `mySystem.api`, not elements from different parents.

2. **Prefer explicit includes**
   - Use narrow includes like `include user`, `include mySystem.webapp`, and `include mySystem.api`.
   - Be cautious with `include mySystem.*` or broader patterns, because they can silently pull in extra containers such as a database, queue, or worker.

3. **Render the actual view**
   - Preview the detail view and check that only the intended three nodes appear.
   - If you see extra nodes or relationships, the include pattern is too broad or another element is being inherited indirectly.

4. **Check relationship scope**
   - Make sure the view only shows the interactions you want to explain at this level.
   - If unrelated edges dominate the diagram, tighten the includes or split the view.

5. **Final sanity check**
   - Open the Problems panel for unresolved references.
   - Compare the detail view with the broader C2 view and confirm the parent system context is still obvious to a reader.
   - If you maintain a separate view-design checklist, use that after the basic structural check to polish the final scope and layout.
