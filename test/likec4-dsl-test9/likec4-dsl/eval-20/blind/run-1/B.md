`npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template`

To confirm both files were actually filtered in the JSON output:

- Check `stats.filteredFiles` — it should be `2`.
- Check `errors[].file` when errors are present — every reported file should be either `projects/template/system-model.c4` or `projects/template/system-views.c4` (or their absolute-path equivalents).
- Check `stats.filteredErrors` — this counts only errors from those two filtered files.
- `stats.totalErrors` may be larger than `filteredErrors` if the wider project has other problems, so `filteredFiles: 2` is the key proof that both `--file` filters matched.
