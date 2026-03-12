Usually no.

In this repo, the rule is: **check shared specs first and reuse an existing kind whenever possible**. A one-off kind such as `Container_UploadOrchestrator` is discouraged if an existing shared kind already covers the need, such as `Container_Api` for an upload service.

Before adding any new kind:

1. Verify the declared shared kinds first (or, in a normal workflow, inspect them via `read-project-summary`).
2. Reuse an existing shared kind if it fits.
3. Only if nothing suitable exists, ask for approval before introducing a new kind.
4. Add the new kind to the shared spec rather than creating a project-specific one-off kind.