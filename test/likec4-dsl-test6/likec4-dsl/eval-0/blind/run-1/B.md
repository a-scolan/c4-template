`npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template`

The key JSON fields are:
- `filteredErrors`: errors found only in the file(s) passed with `--file`
- `filteredFiles`: how many source files actually matched your `--file` filter
- `totalErrors`: errors across the entire project

Interpretation:
- If `filteredErrors > 0`, your edited file failed validation.
- If `filteredErrors = 0` but `totalErrors > 0`, your file is clean and something else in the project is broken.
- If `filteredErrors > 0` and `totalErrors > filteredErrors`, your file failed and other files are failing too.