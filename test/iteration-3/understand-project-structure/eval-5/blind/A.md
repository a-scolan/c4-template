No. `projects/spec-showcase/container-views.c4` is useful as a pattern reference, but it is not the authoritative taxonomy for another project. The repo `README.md` explicitly treats example projects such as `projects/spec-showcase/` and `projects/template/` as pedagogical references, while `projects/shared/` is the automation-facing semantic source.
Validate this first:
1. confirm the active project (`list-projects` -> `read-project-summary`; offline, match the intended `projects/<project>/likec4.config.json`),
2. confirm that project includes `../shared`,
3. confirm the actual container kinds in `projects/shared/spec-containers.c4`, such as `Container_Api` and `Container_Queue`,
4. confirm the valid model relationships in `projects/shared/spec-global.c4`, for example `calls` and `async`,
5. then inspect the target model/view files in that project.
So yes, reuse the pattern idea from `spec-showcase`; no, do not reuse it as semantic truth. Example files are inspiration, while shared specs plus the active project's summary are the source of valid kinds and relationships.
