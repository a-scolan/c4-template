npx likec4 check --format json --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json

- `filteredFiles`: how many files from your `--file` filters were actually included in the filtered diagnostic scope.
- `filteredErrors`: how many errors are associated with that filtered scope only.
- `totalErrors`: how many errors were found overall (full check scope), before/independent of file filtering.

If `filteredFiles` is `2` instead of `3`, one of the three `--file` targets did not participate in the filtered results (for example: wrong path, file not recognized in the active check scope, or not producing diagnostics in that run).