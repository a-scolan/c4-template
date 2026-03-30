npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json projects/template

- `filteredFiles`: how many provided `--file` paths were actually treated as LikeC4 source files for filtering.
- `filteredErrors`: validation errors found only within that filtered subset.
- `totalErrors`: validation errors across the entire project model.

If `filteredFiles` is `2` instead of `3`, it means one of the `--file` arguments was not a DSL source file for validation (here, `likec4.config.json`), so only the two `.c4` files were counted.