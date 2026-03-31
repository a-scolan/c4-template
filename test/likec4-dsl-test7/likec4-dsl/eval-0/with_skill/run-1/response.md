`npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template`

Use these JSON fields:
- `filteredFiles`: should be `1` (confirms only your file was in scope).
- `filteredErrors`: errors in the filtered file(s) only (your file status).
- `totalErrors`: errors across the whole project.

Interpretation:
- `filteredErrors > 0` => your file failed.
- `filteredErrors = 0` and `totalErrors > 0` => your file is clean, but the project is broken elsewhere.
- `filteredErrors = totalErrors` (with `filteredFiles = 1`) => all current project errors come from your file.