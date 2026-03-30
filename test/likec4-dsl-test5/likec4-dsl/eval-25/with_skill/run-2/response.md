npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json projects/template

`filteredFiles`: how many passed `--file` paths were actually DSL source files included in validation.
`filteredErrors`: how many validation errors are in that filtered subset only.
`totalErrors`: how many validation errors exist across the whole project model.

If `filteredFiles` is `2` instead of `3`, it means one of the `--file` paths was not a `.c4`/`.likec4` model source (here, `likec4.config.json`), so it is not counted as a DSL validated file.