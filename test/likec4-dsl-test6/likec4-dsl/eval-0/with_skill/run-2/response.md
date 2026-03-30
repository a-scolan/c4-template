Run from the repo root:

`npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template`

Use these JSON fields:
- `filteredErrors`: errors in the file(s) matched by `--file`; if this is greater than `0`, your edited file failed.
- `totalErrors`: errors across the whole project model; if this is high while `filteredErrors` is `0`, the wider project is broken but your file is clean.
- `filteredFiles`: confirms how many source files were actually matched by the `--file` filter.