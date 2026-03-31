npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json projects/template

- `filteredFiles`: the number of `.c4`/`.likec4` source files actually included by your repeated `--file` filters.
- `filteredErrors`: the number of validation errors found only in that filtered subset.
- `totalErrors`: the number of validation errors across the entire project model.

If `filteredFiles` is `2` instead of `3`, it means one of the three `--file` arguments was not counted as a LikeC4 DSL source file. In this case, `projects/template/likec4.config.json` is config, not a `.c4`/`.likec4` source file, so only the two model/view files count toward `filteredFiles`.
