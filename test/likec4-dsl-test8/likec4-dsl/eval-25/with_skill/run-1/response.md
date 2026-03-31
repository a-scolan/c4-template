npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json projects/template

- `filteredFiles`: how many of the paths passed via repeated `--file` were actually included as LikeC4 DSL source files in the validation filter.
- `filteredErrors`: how many validation errors were found only within that filtered subset.
- `totalErrors`: how many validation errors exist across the entire project model, not just the filtered subset.

If `filteredFiles` comes back as `2` instead of `3`, it means only two of the three `--file` paths were counted as `.c4`/`.likec4` source inputs for DSL validation. In this case, `projects/template/likec4.config.json` is a project config file, not a LikeC4 DSL source file, so it does not count toward `filteredFiles`.