npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json projects/template

- `filteredFiles`: how many `.c4` / `.likec4` source files were actually included by the repeated `--file` filters.
- `filteredErrors`: how many validation errors were found only within that filtered subset.
- `totalErrors`: how many validation errors exist across the entire project model, including files outside the filtered subset.

If `filteredFiles` is `2` instead of `3`, it means one of the three `--file` arguments was not a LikeC4 DSL source file counted by the validator. In this case, `projects/template/likec4.config.json` is config, not a `.c4` / `.likec4` source file, so it would not be included in the DSL file count even though you passed it on the command line.