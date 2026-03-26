`configure-project-includes` is enough for include-path and shared-source wiring, but not enough for the full "add a second project" workflow.

Use it for:
- `likec4.config.json` include/import correctness
- shared specs/images resolution rules

Combine it with a project-structure skill/process for:
- creating the second project folder baseline
- partitioning model/view files
- cross-project naming and ownership conventions

Practical answer: combine it. Keep `configure-project-includes` for import safety, and add a multi-project organization workflow for structure/governance.For adding a second LikeC4 project with shared specs, this skill is necessary but not sufficient.

- `configure-project-includes` is the right core skill for safe `include.paths` and `imageAliases` behavior.
- You should combine it with a workspace/project-organization skill to set folder boundaries, per-project configs, and ownership of shared sources.

Practical split:

- Use include/config rules here to keep imports and icons stable.
- Use multi-project organization guidance to define how projects coexist (naming, root config boundaries, shared folder contracts, and collision policy).

So: use this skill for import safety, plus a multi-project structuring skill for full setup.