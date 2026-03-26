No—creating a one-off `Container_UploadOrchestrator` kind is usually a bad idea here.

Rule of thumb: create a new kind only when multiple elements share stable semantics, common style/constraints, and you want that taxonomy reused across the model. For a single service, use an existing kind (typically `container`) and name/tag it clearly.

Before adding a new kind, first:
1. Check existing specification kinds and reuse one if possible.
2. Confirm at least a few elements will use the new kind.
3. Define the kind consistently in the specification layer before using it in model files.