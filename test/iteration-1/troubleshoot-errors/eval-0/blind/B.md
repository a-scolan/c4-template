Treat these as two independent root-cause checks, not one naming problem.

1. Validate the kind against the shared specification.
   `Container_WebUi` is not declared in the shared container spec. The available UI-oriented kinds include `Container_Webapp`, `Container_Spa`, and `Container_Browser`, so `Container_WebUi` is simply invalid in this project.

2. Validate the element ID separately.
   `Element not found: api` usually means the reference is too short. In the template model, `api` is declared under `mySystem`, so the usable FQN is `mySystem.api` when referenced from outside that parent scope.

3. Diagnose from declarations, not labels.
   Start with `read-project-summary` if available, or inspect the shared specs and the actual declarations in `system-model.c4`. That lets you confirm the valid kinds and the real element IDs before changing anything.

So the likely correction is:
- replace `Container_WebUi` with the valid kind that matches the intent, most likely `Container_Webapp`
- replace `api` with `mySystem.api` wherever a full FQN is required

The key point is that the kind error and the FQN error have different root causes, so fix them independently instead of renaming both blindly.
