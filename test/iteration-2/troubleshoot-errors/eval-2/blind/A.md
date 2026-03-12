Diagnose the two errors separately, starting from the taxonomy rather than renaming at random.

1. Check the relationship taxonomy first
   - In this workspace, the model relationship kinds are `uses`, `calls`, `async`, `reads`, and `writes`.
   - Verify that against the shared specs or `read-project-summary` before changing syntax.
   - `sends` is not one of the defined model relationship types, so it must be corrected rather than accepted as-is.
   - If the intent is messaging or publication, the likely fix is `-[async]->` with a `technology` such as `AMQP`.
   - If it is a synchronous request, use `-[calls]->` instead.

2. Verify the FQN independently
   - `Element not found: dataLayer.cache` may mean the element does not exist, or that the path is not the real fully qualified name.
   - Check the declaration site and confirm the exact FQN from the model tree or project summary.
   - The correct name might be something like `system.cache` or `system.dataLayer.cache` — but do not guess; verify it.

Targeted fix:
- Replace `sends` with the correct defined relationship kind based on the actual interaction.
- Update `dataLayer.cache` only after confirming whether that element exists and what its exact FQN is.
- The root cause may be both a wrong relationship kind and a broken reference, so fix each on its own evidence.
