Run this from the repo root:

```bash
npx likec4 check projects/template/system-model.c4 --format json
```

This validates syntax + semantic model diagnostics for that file scope (without touching manual layout output).

In the JSON output, use these fields to distinguish file-local vs project-wide breakage:

- `summary.errorCount` (overall error total)
- `diagnostics[]` (or `issues[]`, depending on CLI version)
  - `file` / `source.path` (which file each error belongs to)
  - `severity` (error/warning)
- `summary.filesWithErrors` (if present)

Interpretation:

- **Only your file failed**: all `error` diagnostics point to `projects/template/system-model.c4`.
- **Project is broken**: `error` diagnostics reference additional files (or parser/spec errors with no single-file source).