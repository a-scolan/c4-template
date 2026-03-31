npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json projects/template

- `filteredFiles`: how many files were actually included by the repeated `--file` filters for DSL validation.
- `filteredErrors`: how many validation errors are in just that filtered subset.
- `totalErrors`: how many validation errors exist across the entire `projects/template` LikeC4 project.

If `filteredFiles` comes back as `2` instead of `3`, it means only two of the three `--file` paths were counted as LikeC4 source files for validation. In this case, that usually means `projects/template/likec4.config.json` was ignored by the DSL file filter because it is project config, not a `.c4`/`.likec4` model source file.