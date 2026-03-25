```bash
npx likec4 validate --files projects/template/system-model.c4 projects/template/system-views.c4 --no-layout-drift --json
```

To confirm both files were truly filtered in JSON output, verify that the **only** file paths present in reported diagnostics/results are:

- `projects/template/system-model.c4`
- `projects/template/system-views.c4`

If any additional path appears in the JSON, the file filter was not applied correctly.