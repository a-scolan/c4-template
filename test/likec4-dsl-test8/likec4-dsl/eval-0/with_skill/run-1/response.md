npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template

Use these JSON fields:

- `filteredFiles`: should be `1` to confirm only `projects/template/system-model.c4` was included by the `--file` filter.
- `filteredErrors`: errors in your filtered file only.
- `totalErrors`: errors across the whole project.

Interpretation:

- If `filteredErrors > 0`, your file failed validation.
- If `filteredErrors == 0` and `totalErrors > 0`, your file is clean but the project is broken somewhere else.
- If `filteredErrors == 0` and `totalErrors == 0`, both your file and the project are clean.
