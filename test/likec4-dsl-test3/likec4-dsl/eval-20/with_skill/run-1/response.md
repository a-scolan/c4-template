```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template 2>/dev/null
```

To confirm both edited files were actually filtered, check these JSON fields:

- `stats.filteredFiles` should be `2` (both `--file` filters were applied).
- `stats.filteredErrors` is the number of errors coming only from those two files.
- Compare with `stats.totalErrors`: if `filteredErrors` is `0` but `totalErrors` is high, your two files are clean and other files in the project are broken.
- `valid` reflects overall validation status, so use the `stats.*` fields above to verify file-level filtering.