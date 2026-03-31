```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template
```

To confirm both files were actually filtered in the JSON output, check:

- `stats.filteredFiles` is `2`.
- `stats.filteredErrors` counts only errors from those two files.
- `errors[].file` entries, if any, point only to `projects/template/system-model.c4` and/or `projects/template/system-views.c4` (often shown as absolute paths ending with those filenames).
- `stats.totalErrors` may be higher than `stats.filteredErrors`; that just means other files in the project have problems, but they were not part of your filter.

A quick pass/fail rule: if `stats.filteredFiles !== 2`, then one of the `--file` filters did not match a validated `.c4` source file.