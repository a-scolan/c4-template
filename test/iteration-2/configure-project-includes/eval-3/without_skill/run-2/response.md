`configure-project-includes` is enough for include-path and shared-source wiring, but not enough for the full "add a second project" workflow.

Use it for:
- `likec4.config.json` include/import correctness
- shared specs/images resolution rules

Combine it with a project-structure skill/process for:
- creating the second project folder baseline
- partitioning model/view files
- cross-project naming and ownership conventions

Practical answer: combine it. Keep `configure-project-includes` for import safety, and add a multi-project organization workflow for structure/governance.