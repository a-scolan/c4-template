Use this command:

`npx likec4 validate projects/template/system-model.c4 projects/template/system-views.c4 --format json --skip-check layout-drift`

To confirm the filter really applied in the JSON output:

1. Check the top-level file filter section (commonly `files`, `filteredFiles`, or a similar input/filter field) and make sure it contains **exactly** these two paths:
   - `projects/template/system-model.c4`
   - `projects/template/system-views.c4`
2. Check every reported diagnostic/result entry and verify its file path is only one of those two files.
3. Confirm there is no `layout-drift` check/result in the JSON at all, which shows that layout drift validation was excluded.
