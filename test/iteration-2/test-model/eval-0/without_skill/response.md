## Validation plan

1. **Check structure and kinds first**
   - Start with `read-project-summary` (or the full model summary in your editor) and confirm the new worker is declared under the expected system, not as a top-level element.
   - Verify the worker uses a valid container kind for its role. In this template, common C2 kinds include `Container_Webapp`, `Container_Api`, `Container_Queue`, `Container_Database`, and `Container_ProcessingServer`.
   - Confirm the dedicated C2 view sits in the right views section and its title/intent match the model change.

2. **Verify FQNs and references**
   - Use `search-element` to confirm the worker's fully qualified name is exactly what the views reference, for example `mySystem.worker`.
   - Check every `include`, `navigateTo`, and relationship endpoint for the same FQN.
   - Make sure there is no mix of local alias vs FQN that accidentally points to a different element.

3. **Validate relationships semantically, not just syntactically**
   - Use `find-relationships` to re-check the worker's incoming and outgoing edges.
   - Use `calls` for synchronous request/response, `async` for fire-and-forget or messaging, and `reads`/`writes` for data access.
   - Verify labels and `technology` still make sense after the change.
   - Confirm no old relationship to the previous container was left behind.

4. **Check impacted views**
   - Render both the main C2 view and the new dedicated C2 view.
   - Confirm the worker appears once, the expected neighbors are present, and no unintended siblings or databases are pulled in by a broad include.
   - Check edge direction, line style, labels, and any `navigateTo` link from the parent view.

5. **Do a pre-commit visual and editor pass**
   - Open the Problems panel and make sure it is clean.
   - Compare before/after rendering or screenshots for the affected C2 views.
   - If layout now looks crowded, tighten the includes before committing.
