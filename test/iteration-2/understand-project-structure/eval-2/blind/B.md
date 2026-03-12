Start from the source of truth, not from guesswork.

## Diagnosis sequence for an unknown kind/relationship error

1. **Check the shared specs first**
   - Kinds for C1: `projects/shared/spec-context.c4`
   - Kinds for C2: `projects/shared/spec-containers.c4`
   - Kinds for C3: `projects/shared/spec-components.c4`
   - Model relationships and global tags: `projects/shared/spec-global.c4`
   - Deployment kinds/relationships: `projects/shared/spec-deployment.c4`
2. **Compare the exact requested identifier against the valid taxonomy**
   - Example kind check: `Container_Api` is valid; `Container_API` is not.
   - Example relationship check: valid model relationships are `uses`, `calls`, `async`, `reads`, and `writes`.
   - Example deployment taxonomy check: `Infra_Fw` is valid; `Infra_Firewall` is not.
3. **Confirm the active project context**
   - Read the target project's `likec4.config.json` and confirm it includes `../shared`.
   - Re-run `list-projects`, then `read-project-summary` for the intended project.
4. **Verify the error in current model context**
   - Check whether the failing declaration is in a system model, a deployment section, or a view.
   - Make sure you are using a model relationship in the model and a deployment relationship only in deployment-specific infrastructure cases.
5. **Only then correct the identifier**
   - Replace the invalid kind/relationship with the exact declared one from the shared specs.

## What to compare before fixing

- Requested kind name vs. declared element/deployment node names in shared specs
- Requested relationship name vs. declared relationship names in `spec-global.c4` or `spec-deployment.c4`
- Intended abstraction level vs. allowed taxonomy:
  - C1 = actors/systems
  - C2 = containers such as `Container_Api`
  - C3 = `Component`

## If the project summary looks inconsistent

Use the fallback from the skill:

1. Re-run `list-projects`.
2. Re-run `read-project-summary` with the explicit project.
3. Verify the project's `likec4.config.json` include paths point to the shared specs you expect.
4. If the summary still disagrees with the specs, stop editing and report the project context as blocked or incomplete.

That keeps the fix rooted in the real workspace taxonomy instead of papering over the symptom.