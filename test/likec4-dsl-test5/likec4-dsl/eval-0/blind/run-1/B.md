Run this from the repo root:

`npx likec4 validate projects/template/system-model.c4 --format json`

In the JSON output, use:
- `issues[*].source.path` (or equivalent file path field) to see exactly which file each error belongs to.
- `summary.errorCount` (or total errors) to confirm whether there are any failures at all.
- `summary.filesWithErrors` / `summary.filesChecked` (if present) to tell whether only `projects/template/system-model.c4` failed or multiple files failed (project-wide breakage).

Quick rule: if every reported issue path is `projects/template/system-model.c4`, your edit is isolated; if issue paths include other files, the project is broadly broken.Run this from the repository root:

```bash
npx likec4 check projects/template/system-model.c4 --format json
```

In the JSON output, look at:

- `summary.valid` (or the top-level pass/fail flag): overall result for the checked scope.
- `summary.filesChecked` and `summary.filesWithErrors`: how many files were evaluated and how many failed.
- Per-file diagnostics (typically under `files`, `diagnostics`, or `issues`) with each record’s `file` path and its errors.

Interpretation:

- **Only your file failed**: exactly one failing file, and its path is `projects/template/system-model.c4`.
- **Whole project is broken**: more than one failing file, or failures include files other than `projects/template/system-model.c4`.

If your CLI version uses different field names, apply the same logic: combine the **overall summary counters** with the **per-file error entries keyed by path**.# LikeC4 Syntax & Semantic Validation — Single File

## CLI Command

LikeC4 does not support single-file validation in isolation because models are cross-referenced across files. The correct command to run **syntax and semantic validation only** (no diagram layout generation) from the repo root is:

```bash
npx likec4 check projects/template/
```

This runs the language-server-backed validation pass for the entire project the file belongs to, without triggering any layout computation or export. If you want to scope it to just the `template` project config:

```bash
npx likec4 check --project projects/template/likec4.config.json
```

> **Note:** There is no `--file` flag that restricts validation to a single `.c4` file, because semantic checks (e.g. element references, relationship targets) require the full project graph to be resolved.

---

## JSON Output Fields to Distinguish File vs. Project Failures

When run with `--reporter json` (or equivalent structured output), each diagnostic entry has the shape:

```json
{
  "severity": "error" | "warning",
  "message": "...",
  "file": "projects/template/system-model.c4",
  "range": {
    "start": { "line": 12, "character": 4 },
    "end":   { "line": 12, "character": 20 }
  }
}
```

### Interpretation

| Condition | What to look for |
|-----------|-----------------|
| **Only your file failed** | All diagnostic objects have `"file": "projects/template/system-model.c4"` |
| **Whole project is broken** | Diagnostics reference multiple distinct `"file"` values, or errors appear in files you did not touch (e.g. `spec-code.c4`, `spec-global.c4`, shared files) |
| **Cross-file semantic error triggered by your edit** | The `"file"` field points to *another* file, but the `"message"` mentions an element ID you defined or removed in `system-model.c4` (broken reference in a consumer file) |

### Key JSON fields

- **`file`** — absolute or workspace-relative path; primary discriminator for "which file owns this error"
- **`severity`** — `"error"` stops the build; `"warning"` is informational
- **`message`** — human-readable description; look for "Cannot resolve reference", "Duplicate name", or "Unknown element kind" to classify the failure type
- **`range`** — pinpoints the exact token; if `line` values are all within plausible bounds for `system-model.c4`, the fault is local

---

## Quick Decision Rule

1. Filter diagnostics where `severity === "error"`.
2. Collect the unique set of `file` values.
3. If that set is `{ "projects/template/system-model.c4" }` → only your file is broken.
4. If the set contains other files → cross-file or project-wide breakage.
