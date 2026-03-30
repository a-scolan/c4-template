`npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template`

In the JSON output, confirm that `filteredFiles` is `2`; that proves both `--file` filters matched LikeC4 source files, while `filteredErrors` then reports only errors from those two files (as distinct from `totalErrors` across the whole project).