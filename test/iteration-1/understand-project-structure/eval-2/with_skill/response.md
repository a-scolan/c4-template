Do not diagnose an unknown kind or unknown relationship by guessing from nearby code. Start from the repository taxonomy and the loaded project context.

## Structured diagnosis

1. **Classify the error first.**
   - Is it an element kind error?
   - A deployment node kind error?
   - A model relationship error?
   - A deployment relationship error?

2. **Check the shared specs before touching the model.**
   - `projects/shared/spec-context.c4` for C1 kinds
   - `projects/shared/spec-containers.c4` for C2 kinds
   - `projects/shared/spec-components.c4` for C3 kinds
   - `projects/shared/spec-global.c4` for model relationships
   - `projects/shared/spec-deployment.c4` for deployment kinds, deployment tags, and deployment-only relationships

3. **Compare the failing token literally against the valid taxonomy.**
   - For model relationships, valid shared values here are `uses`, `calls`, `async`, `reads`, `writes`.
   - For common C2 container work, valid examples include `Container_Api`, `Container_Webapp`, `Container_Database`, `Container_Queue`, `Container_Browser`.
   - For C3, the valid component kind is `Component`.
   - For deployment, compare against deployment node kinds such as `Node_Environment`, `Zone`, `Node_Vm`, `Node_App`, and deployment relationships such as `http`, `https`, `tcp`, `nfs`, `amqp`, `ldap`, `sql`, `redis`, `smtp`, `oidc_saml`.

4. **Confirm the active project has loaded the expected taxonomy.**
   - Re-run `list-projects`.
   - Re-run `read-project-summary` for the explicit project id.
   - Re-read that project's `likec4.config.json` and verify it includes `../shared`.

5. **Check whether the error is really a taxonomy mismatch or a scope mismatch.**
   - A deployment relationship used in the system model will still be wrong even if the name exists.
   - A component kind used where a container belongs will still be wrong even if the kind exists.
   - A valid token in one project is still unsafe if the active project context is stale.

## Confirmation sequence before correction

1. Identify the token that fails.
2. Find the authoritative definition in the correct shared spec file.
3. Confirm the active project via `list-projects` and `read-project-summary`.
4. Confirm the project config includes the shared specs.
5. Only then replace the token with the exact valid local taxonomy.

## Important local rule

Use `SPEC_CHEATSHEET.md` for orientation, but use the `spec-*.c4` files as the final authority. If the cheat sheet and a spec file ever disagree, trust the spec file.

## If the project summary looks inconsistent

1. Re-run `list-projects` and make sure you are targeting the intended project id.
2. Re-run `read-project-summary` with the explicit project.
3. Re-open the project `likec4.config.json` and verify the include paths.
4. Re-check that the shared spec files are the ones the project is meant to load.
5. If the summary still does not match the config and shared specs, stop and treat the context as blocked rather than guessing a fix.