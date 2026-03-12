No—creating `Container_UploadOrchestrator` just for one service is usually the wrong move in this workspace.

The rule here is: check the shared specifications first and reuse an existing kind whenever it already fits the role. For an upload service, `Container_Api` is the obvious first candidate, so a one-off kind would add noise without improving the model.

Before adding any new kind:

1. Check the shared specs under `projects/shared/spec-*.c4` to see whether a suitable kind already exists.
2. Reuse the closest existing kind if it matches the responsibility.
3. Only propose a new kind if there is a real, reusable distinction that will apply in more than one place.
4. Get explicit approval before introducing the new kind.

So in this case, start by modeling the service as a `Container_Api`, not as a custom `Container_UploadOrchestrator`.