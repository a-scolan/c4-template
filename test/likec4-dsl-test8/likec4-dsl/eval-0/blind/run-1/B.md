Run this from the repo root:

```bash
npx likec4 check projects/template/system-model.c4 --format json
```

Use `check`, not `build`, because you want syntax/semantic validation only and do **not** want manual-layout/layout-drift noise.

In the JSON output, use these parts to tell **"only my file failed"** vs **"the project is broken more broadly"**:

- The per-diagnostic file locator field for each error/warning entry — i.e. the field that points to the source file (`path`/`uri`, depending on the emitted shape).
- The top-level diagnostics collection itself (`diagnostics` / per-file results).
- The top-level/project-level status or counts (`status`, `errorCount`, summary counts if present).

Interpretation:

- **Only your file failed**: every reported diagnostic points to `projects/template/system-model.c4`, and there are no failures reported for other files.
- **Whole project is broken**: diagnostics point at additional files, or there is a project-level failure/status indicating the workspace/config/model load failed beyond that one file.

So in practice, first filter diagnostics by their `path`/`uri`, then compare that against the overall `status` / error totals.