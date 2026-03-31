`npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template`

To confirm both files were actually filtered, check the JSON `stats` object:

- `filteredFiles` should be `2` — that means both repeated `--file` filters matched LikeC4 source files.
- `filteredErrors` is the number of errors only inside those two filtered files.
- `totalErrors` is the error count across the whole project, so it can be higher than `filteredErrors`.

If `filteredFiles` is not `2`, at least one `--file` path did not match a `.c4`/`.likec4` source file in that project scope.