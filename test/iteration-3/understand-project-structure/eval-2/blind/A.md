Structured diagnosis for an unknown kind/relationship error:
1. Classify the token first.
- Element kind/tag problem: check `projects/shared/spec-context.c4`, `spec-containers.c4`, `spec-components.c4`, or `spec-deployment.c4`
- Model relationship problem: check `projects/shared/spec-global.c4`
- Deployment relationship problem: check `projects/shared/spec-deployment.c4`
2. Check the active project's `likec4.config.json` and confirm it includes `../shared`. In this repo both visible projects do, so taxonomy should be shared if the correct project is active.
3. Compare the exact token against the shared spec declaration: same casing, same underscores, same singular/plural. This workspace uses exact PascalCase names for kinds/tags.
4. Confirm the usage context:
- `kind is ...` in a view filter must match a declared kind name exactly
- `view ... of <container>` must reference a container ID that exists in the active project model
- Deployment node kinds/relationships belong in deployment modeling, not in the core system model
5. Use the spec file itself as the final authority, not summaries or examples. The repo already shows why: `SPEC_CHEATSHEET.md` drifts from the actual shared specs (`Container_ObjectStorage` in `spec-containers.c4`, not `Storage`; `Container_DatabaseGeo`, not `Container_Database_Geo`).
6. Only after the token matches the source-of-truth spec should you update the model/view.

Short version: check active project -> check shared include -> check exact token in the right shared spec -> check that the token is being used in the right modeling layer.
