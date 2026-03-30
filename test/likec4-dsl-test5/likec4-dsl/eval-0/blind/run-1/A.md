npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template

Use these JSON fields:
- `filteredFiles`: how many files were actually included by your `--file` filters.
- `filteredErrors`: errors only in that filtered subset (your edited file(s)).
- `totalErrors`: errors across the whole project.

Interpretation:
- `filteredErrors > 0` means your target file failed.
- `filteredErrors = 0` but `totalErrors > 0` means your file is clean, but other files in the project are broken.