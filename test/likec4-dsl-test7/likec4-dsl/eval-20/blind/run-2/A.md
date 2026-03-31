npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template

To confirm both files were actually filtered in the JSON output, check `stats.filteredFiles`:

- `filteredFiles: 2` means both `--file` filters matched LikeC4 source files.
- `filteredErrors` counts errors only from those two filtered files.
- `totalErrors` counts errors across the whole project, so it can be higher than `filteredErrors` without meaning the filter failed.

Because both inputs here are `.c4` files, the expected confirmation is `"filteredFiles": 2`.