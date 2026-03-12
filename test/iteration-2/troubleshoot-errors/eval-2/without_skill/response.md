Diagnose those as **two separate checks**: one for the relationship taxonomy, one for the FQN.

1. **Check the relationship taxonomy first.** In this workspace, the shared model relationships from `projects/shared/spec-global.c4` are `uses`, `calls`, `async`, `reads`, and `writes`. Deployment-only relationships from `projects/shared/spec-deployment.c4` include things like `http`, `https`, `tcp`, `amqp`, `sql`, `redis`, and `smtp`.

   `sends` is **not** one of the defined relationship kinds here, so `Unknown relationship type: sends` is a real taxonomy problem. Do not accept it as-is.

   Pick the relationship that matches the actual meaning:
   - `calls` for synchronous invocation
   - `async` for queue/message publishing
   - `reads` / `writes` for data access

2. **Check the FQN separately.** `Element not found: dataLayer.cache` means that exact path is not present in the model. Verify:
   - does `dataLayer` actually exist?
   - is `cache` really nested under `dataLayer`?
   - or is the real FQN something else, such as a sibling under another parent?

3. **Then apply a targeted fix.**
   - Replace `sends` with the correct defined relationship kind.
   - Replace `dataLayer.cache` with the real FQN, or define `cache` under `dataLayer` if that nesting was intended.

So the right diagnosis is very likely **both**:
- `sends` is an invalid relationship name in this workspace, and
- `dataLayer.cache` may be a broken or non-existent FQN.

Fix the taxonomy and the element path independently instead of doing blind renaming.