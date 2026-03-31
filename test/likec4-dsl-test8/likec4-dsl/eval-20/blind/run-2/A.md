Use a single filtered validation command with JSON output and layout drift disabled:

```bash
npx likec4 validate --json --no-layout-drift --files projects/template/system-model.c4 projects/template/system-views.c4
```

To confirm the filter really applied in the JSON output:

- Check the file filter section/top-level file list in the JSON and verify it contains **exactly** these two paths:
  - `projects/template/system-model.c4`
  - `projects/template/system-views.c4`
- Then verify every reported diagnostic/location path in the JSON belongs to one of those two files.
- If any other `.c4` file appears anywhere in the reported file paths, the filter was **not** limited to just the two edited files.

In short: the JSON should mention only those two target files, both in the echoed filtered file set and in any diagnostic `file`/`path` entries.