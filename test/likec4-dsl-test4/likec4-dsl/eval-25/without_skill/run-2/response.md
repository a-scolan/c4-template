```
npx likec4 lint --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json
```

**`filteredFiles`** — the number of files among those passed via `--file` that actually contain at least one diagnostic (warning or error). A file with no issues is counted in the total processed but not here.

**`filteredErrors`** — the total count of error-level diagnostics found across only the files listed with `--file`. Warnings are excluded from this count (or reported separately depending on the CLI version).

**`totalErrors`** — the overall count of all errors found in the entire project (all files the language server resolves, not just the `--file` subset). If your three files cross-reference shared spec files that have errors, those would appear here but not in `filteredErrors`.

**If `filteredFiles` comes back as `2` instead of `3`** — one of the three files was clean (zero diagnostics). The CLI only counts a file in `filteredFiles` when it produced at least one diagnostic. This means one of your three edited files has no syntax or semantic issues, and the other two do.
