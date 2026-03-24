Treat this as a semantic validation, not just a parser check:
1. Confirm both container FQNs still resolve and that the `async` relationship is the only intended edge between them; remove any leftover `calls` edge that would make the flow ambiguous.
2. Check the meaning of the relationship: `async` should represent fire-and-forget, queued, or event-driven behavior. Do not add a fake return path that makes the interaction look synchronous.
3. Keep protocol details in `technology`, not in the edge type, and give the edge a clear label so the message or event is obvious in the C2 view.
4. Preview the impacted C2 view and confirm the parent system boundary and expected neighbors are still present; if the view looks odd, inspect include scope and any layout hints before assuming the model is wrong.
5. Make sure normal application traffic still lives in the logical model and has not been redrawn in deployment just to compensate for the visual change.

If those checks pass, the model is probably truly correct, not merely syntactically acceptable.
