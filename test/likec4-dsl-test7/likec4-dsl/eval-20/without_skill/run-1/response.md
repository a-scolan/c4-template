Use this single command:

```bash
npx likec4 validate --files projects/template/system-model.c4 projects/template/system-views.c4 --format json --skip-layout-drift
```

To confirm both files were actually filtered, inspect the JSON payload and verify the file-scope list contains exactly these two paths (and no others). In practice, check the field that reports selected/validated files (for example `files`, `filteredFiles`, or equivalent in your LikeC4 version) and ensure both entries are present:

- `projects/template/system-model.c4`
- `projects/template/system-views.c4`

If that list has only those two files, the filter was applied correctly.