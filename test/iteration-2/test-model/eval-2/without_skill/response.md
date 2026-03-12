## Validate the model, not just the parser result

1. **Re-check the exact endpoints**
   - Start with `read-project-summary` (or the full model summary in your editor) and confirm the two containers are still the intended FQNs.
   - Use `find-relationships` to verify there is one `async` edge between the exact containers where the old `calls` edge used to be.

2. **Test the semantics of the change**
   - Ask whether the interaction is truly asynchronous.
   - If the sender publishes work and does not wait for a response, `async` is reasonable.
   - If the sender still needs an immediate reply, `calls` was the right model and the new relationship is only syntactically valid, not semantically correct.
   - Re-check the `technology` label too: `AMQP`, a queue, an event bus, or webhook-style delivery usually fit better than plain `HTTPS` request/response.

3. **Compare before and after in views**
   - Render every affected view: the focused C2 view, the broader container view, and any other view that includes those containers.
   - Compare line style, arrow direction, labels, and layout before and after the change.
   - If the diagram now looks odd, verify whether the model is missing an intermediate queue or broker container that would make the async flow explicit.

4. **Inspect downstream impact**
   - Check whether other views or documentation still describe the interaction as synchronous.
   - Make sure the new relationship does not create contradictory edges or duplicate paths in dependent views.

5. **Do the pre-commit checks**
   - Confirm the Problems panel is clean.
   - Use a quick visual diff or screenshot comparison for the impacted views.
   - Only keep the `async` change if both the semantics and the rendered views still tell the right story.
