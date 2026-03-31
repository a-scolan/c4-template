npx likec4 validate --json --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json

- `filteredFiles`: how many of the paths passed via `--file` were actually matched and included in the filtered validation scope.
- `filteredErrors`: how many validation errors are attributed to that filtered scope.
- `totalErrors`: how many validation errors exist overall in the loaded validation run, including errors outside the filtered subset.
- If `filteredFiles` is `2` instead of `3`, one of the three requested paths did not end up in the validator's filtered file set. In practice, that usually means one path did not resolve/match as expected, or a file such as `projects/template/likec4.config.json` was not counted as a validated model source file in that summary.