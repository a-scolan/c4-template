```
npx likec4 validate --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json
```

**`filteredFiles`** — the number of files among those you passed via `--file` that actually contained at least one diagnostic (error or warning). It tells you which files have issues.

**`filteredErrors`** — the total count of errors found specifically inside the files you listed with `--file`. This is the subset of all errors that belong to your edited files.

**`totalErrors`** — the overall error count across the entire model (all files the project loads, not just the filtered ones). A non-zero `totalErrors` with zero `filteredErrors` means errors exist elsewhere in the project, not in your changes.

**If `filteredFiles` is `2` instead of `3`**: one of your three listed files was either not found (wrong path, file not saved), not parsed by the validator (e.g. `likec4.config.json` may be excluded from DSL validation because it is JSON config, not a `.c4` source file), or contained no diagnostics and was therefore not counted. Most likely the config file is not treated as a LikeC4 DSL source and is skipped by the validator.
