npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json projects/template

- `filteredFiles`: how many files were actually included by the repeated `--file` filters.
- `filteredErrors`: how many validation errors are in that filtered subset only.
- `totalErrors`: how many validation errors exist across the whole project model, not just the filtered files.

If `filteredFiles` is `2` instead of `3`, that means only two of the three `--file` inputs were counted as LikeC4 source files for DSL validation. In this case, the usual reason is that `projects/template/likec4.config.json` is project config, not a `.c4`/`.likec4` source file, so it does not contribute to the filtered DSL file count.