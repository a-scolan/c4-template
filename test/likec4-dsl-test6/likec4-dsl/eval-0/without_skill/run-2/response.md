Run this from the repository root:

```bash
npx likec4 validate projects/template/system-model.c4 --json
```

That validates the specified file for syntax and semantic/model errors only; it does not do layout comparison or layout drift checks.

In the JSON output, use these parts to decide whether the failure is isolated to your file or indicates a broader project problem:

- `diagnostics[*].location.path` (or the equivalent file-path field in your CLI version): which file each error belongs to.
- `diagnostics[*].severity`: whether the entry is an error vs. warning.
- Top-level/project-level status fields such as `ok`, `valid`, or `summary.errorCount` (name can vary slightly by version): whether the overall validation run succeeded.

Practical rule:

- If all error diagnostics point only to `projects/template/system-model.c4`, then only your edited file failed.
- If diagnostics also reference other `.c4` files, or the project-level status is failed because of errors outside that file, then the project is broken more broadly.

If you want to be extra strict in automation, filter the diagnostics by `location.path` and fail only when paths other than `projects/template/system-model.c4` appear.