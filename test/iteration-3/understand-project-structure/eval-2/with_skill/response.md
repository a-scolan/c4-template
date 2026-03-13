Structured diagnosis for an unknown kind/relationship error:
1. Start from the source of truth, not from memory: the active project's summary plus `projects/shared/spec-*.c4`. Use `projects/shared/SPEC_CHEATSHEET.md` only as a quick index.
2. Compare the exact failing token against the declared taxonomy:
- kinds in `spec-context.c4`, `spec-containers.c4`, `spec-components.c4`, `spec-deployment.c4`
- model relationships in `spec-global.c4`
- deployment relationships in `spec-deployment.c4`
3. Check for scope confusion: deployment relationships such as `https` or `amqp` belong to deployment modeling, while system-model relationships here are `uses`, `calls`, `async`, `reads`, `writes`.
4. Check for naming drift between a quick reference and the actual spec files. In this repo, `SPEC_CHEATSHEET.md` mentions `Container_Database_Geo`, but `projects/shared/spec-containers.c4` declares `Container_DatabaseGeo`; the spec file wins.
5. Confirmation sequence before correction: revalidate the active project, re-run `read-project-summary`, confirm the project `likec4.config.json` includes `../shared`, confirm the exact kind/relationship in the relevant shared spec, inspect the nearby model/view file to verify parent and context, and only then fix the model.
If the project summary looks inconsistent, re-run `list-projects`, re-run `read-project-summary` with the explicit project ID, re-check `likec4.config.json` include paths, verify the shared specs are reachable, and stop as blocked if the context still disagrees. `.github/skills/` can guide workflow, but it is not the source of valid kinds or relationship names.
