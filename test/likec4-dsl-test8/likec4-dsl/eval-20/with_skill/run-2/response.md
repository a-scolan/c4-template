```bash
likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template
```

To confirm both files were actually filtered in the JSON output:

- Check that `"filteredFiles": 2` — this proves both `--file` arguments matched LikeC4 source files and were included in the filtered validation set.
- Check `"filteredErrors"` for the error count limited to those two files only.
- Compare with `"totalErrors"`, which is the error count across the whole project and may be higher.

If `filteredFiles` is not `2`, then at least one `--file` path did not match a `.c4`/`.likec4` source file in the validated project scope.