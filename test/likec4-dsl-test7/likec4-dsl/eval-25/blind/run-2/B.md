npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json projects/template

- `filteredFiles`: how many `.c4`/`.likec4` source files were actually included by the repeated `--file` filters.
- `filteredErrors`: how many validation errors were found only within that filtered subset.
- `totalErrors`: how many validation errors exist across the entire project model, not just the filtered subset.

If `filteredFiles` is `2` instead of `3`, it means one of the paths you passed with `--file` was not counted as a LikeC4 DSL source file. In this case, `projects/template/likec4.config.json` is a project config file, not a `.c4`/`.likec4` file, so it does not increase `filteredFiles`.