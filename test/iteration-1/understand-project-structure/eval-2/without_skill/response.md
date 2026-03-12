## Structured diagnosis for an unknown kind or relationship error

1. **Start from the source of truth, not from memory or examples.**
   - Element kinds are defined in `projects/shared/spec-context.c4`, `projects/shared/spec-containers.c4`, and `projects/shared/spec-components.c4`.
   - Deployment node kinds and deployment-only relationships are defined in `projects/shared/spec-deployment.c4`.
   - Model relationships are defined in `projects/shared/spec-global.c4`.

2. **Classify the failing token before fixing anything.**
   - Is it a C1 element kind?
   - A C2 container kind?
   - A C3 component kind?
   - A deployment node kind?
   - A model relationship or a deployment relationship?

3. **Compare the exact token against the valid taxonomy.**
   - Check spelling, capitalization, separators, and suffixes.
   - Examples from this repository:
     - `Container_Api` is valid.
     - `Component` is valid.
     - `uses`, `calls`, `async`, `reads`, and `writes` are valid model relationships.
     - `http`, `https`, `tcp`, `nfs`, `amqp`, `sql`, `ldap`, `redis`, `smtp`, and `oidc_saml` are deployment-side relationships.

4. **Confirm the file is using the token at the correct modeling level.**
   - C1/C2/C3 model files should use model kinds and model relationships.
   - Deployment sections should use deployment node kinds and deployment-side relationships.
   - A valid token in the wrong context can still trigger the error.

5. **Verify project wiring before correction.**
   - Check that the target project’s `likec4.config.json` includes `../shared`.
   - Check that the file you are editing belongs to the intended project.
   - Compare the failing usage with a known-good example in the same repository, such as `projects/template/system-model.c4`.

6. **Only then choose the correction.**
   - Replace the invalid token with the exact valid one from the shared specs.
   - If the intended concept is missing entirely, do not invent a near match; decide whether the shared taxonomy needs a deliberate extension.

## Fallback if any generated summary looks inconsistent

- Trust the raw shared spec files and the project config over any secondary summary.
- Re-open the target project files and compare them directly with the shared definitions.
- If needed, use `projects/shared/SPEC_CHEATSHEET.md` as a quick cross-check, but treat the raw `.c4` spec files as final authority.
