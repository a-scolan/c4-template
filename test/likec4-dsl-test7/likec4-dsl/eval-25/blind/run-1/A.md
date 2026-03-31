npx likec4 check --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json

- `filteredFiles`: how many of the files you explicitly passed with `--file` were actually included in this validation run.
- `filteredErrors`: how many reported errors belong to those filtered files only.
- `totalErrors`: how many errors exist in the whole analyzed project scope before (or regardless of) file filtering.

If `filteredFiles` is `2` instead of `3`, one of your three `--file` targets was not part of the effective validation set (commonly a wrong path, a file not found/resolved, or a file not included by project configuration), so only two files were actually checked under the filter.