npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template

In the JSON output, confirm `filteredFiles` is `2` (both `--file` filters were applied) and use `filteredErrors` to see errors only in those two files. `totalErrors` still reflects errors across the entire project.