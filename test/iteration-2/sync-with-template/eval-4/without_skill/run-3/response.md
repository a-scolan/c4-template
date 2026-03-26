## Checks after syncing with the template

Run these checks before you trust the result:

1. Confirm the project still parses with the updated shared specs and config.
2. Confirm includes resolve to the expected shared files.
3. Inspect representative context, container, component, and deployment views.
4. Check for missing or renamed tags, element kinds, and relationship kinds.
5. Check view filters that depend on tags or kinds.
6. Verify that instance mappings and deployment modeling still match the logical model.
7. Look for obvious semantic drift: wrong labels, wrong technologies, or relationships that no longer describe reality.
8. Review any ADR or local documentation that references template behavior.

A useful final sanity pass is to ask: does the rendered workspace still express the same architecture, just with newer shared vocabulary and defaults? If yes, the sync was probably healthy.