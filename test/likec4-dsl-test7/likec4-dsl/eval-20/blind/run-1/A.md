`npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template`

To confirm both files were actually filtered in the JSON output:

- Check that `stats.filteredFiles` is `2`.
- Check that `stats.filteredErrors` reports errors only from those two files.
- `stats.totalErrors` can be higher, because it counts errors across the full project, not just the filtered files.
- If `filteredFiles` is not `2`, one of the `--file` paths did not match a LikeC4 source file as expected.