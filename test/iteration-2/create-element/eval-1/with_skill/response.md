No—creating a one-off `Container_UploadOrchestrator` kind just for one service is not the rule in this workspace.

Use the shared-spec-first approach:

1. Check the existing shared kinds in `projects/shared/spec-*.c4` first.
2. Reuse the closest declared kind if one already fits the need.
3. Only consider a new kind if nothing suitable exists.
4. Ask for approval before introducing any new kind.

In practice, avoid one-off custom kinds when an existing container kind already covers the service.