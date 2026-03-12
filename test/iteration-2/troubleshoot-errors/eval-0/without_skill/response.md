Treat those as **two separate root-cause checks**, not one mystery.

1. **Verify the kind taxonomy first.** In this workspace, the shared container kinds come from `projects/shared/spec-containers.c4`, and they include names such as `Container_Webapp`, `Container_Spa`, `Container_Browser`, and `Container_Api`. `Container_WebUi` is **not** one of the defined kinds, so that error is a real taxonomy problem, not a spelling quirk that LikeC4 should tolerate.

2. **Verify the element path separately.** `Element not found: api` usually means the element exists, but **not at the scope you referenced**. In this template, containers typically live under a parent system, so the correct reference is often a full FQN such as `system.api` or `mySystem.api`, not bare `api`, unless you are already inside that parent scope.

3. **Diagnose from the model structure, not by random renaming.** Start from the actual project summary / model tree and shared specs:
   - Which kinds are actually defined?
   - What is the exact full path of the element?

4. **Targeted fix:**
   - Replace `Container_WebUi` with a valid kind that matches the intent, most likely `Container_Webapp` if it is a web application.
   - Replace `api` with the real FQN, for example `system.api` or `mySystem.api`, or define that element under the expected parent if it does not exist yet.

So the likely diagnosis is: **invalid kind + incorrect FQN reference**. Fix those directly before changing anything else.