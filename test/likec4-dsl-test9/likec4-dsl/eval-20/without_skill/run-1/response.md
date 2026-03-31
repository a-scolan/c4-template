Use this command:

```bash
npx likec4 validate --json --files projects/template/system-model.c4 --files projects/template/system-views.c4 --no-layout-drift
```

To confirm the filter worked in the JSON output:

- Verify the JSON reports exactly these two file paths in its filtered/input file list.
- Verify that count is `2`.
- If the JSON includes diagnostics, every diagnostic `path` must be either `projects/template/system-model.c4` or `projects/template/system-views.c4`.
- Because layout drift checks are disabled, there should be no layout-drift entries in the JSON output.
