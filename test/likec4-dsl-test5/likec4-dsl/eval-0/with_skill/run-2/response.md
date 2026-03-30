```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template
```

Use these JSON fields:
- `filteredErrors`: errors in the `--file`-filtered subset (your edited file here).
- `filteredFiles`: how many source files were actually filtered.
- `totalErrors`: errors across the entire project model.

Interpretation:
- `filteredErrors > 0` means your filtered file failed.
- `filteredErrors = 0` but `totalErrors > 0` means your file is clean, while something else in the project is broken.