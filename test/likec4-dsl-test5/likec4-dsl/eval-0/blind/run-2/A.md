Run from the repo root:

`npx likec4 validate projects/template/system-model.c4 --format json`

In the JSON output, check:
- `diagnostics[*].source.path` (or equivalent path field) to see exactly which file(s) failed.
- `summary.errorCount` (or equivalent summary errors count) to see whether validation failed overall.

If all diagnostics point only to `projects/template/system-model.c4`, your edit is the isolated failure. If diagnostics include additional files, the project is broken more broadly.# LikeC4 Syntax & Semantic Validation — Targeted File Check

## CLI Command

To run syntax and semantic validation **without triggering layout computation or layout drift**, use the `check` command (not `build`):

```bash
npx likec4 check projects/template/
```

To get machine-readable output, add `--json` (or `--format json` depending on CLI version):

```bash
npx likec4 check --json projects/template/
```

The `check` command validates DSL syntax, semantic correctness (element references, relationship targets, kind conformance), and model integrity — but does **not** run the layout engine, so no layout drift is introduced.

> **Note:** LikeC4's `check` command validates the whole project graph because elements in `system-model.c4` may be referenced by other files (e.g. shared specs or views). There is no single-file isolation flag in the standard CLI; the project must be parsed as a whole to resolve cross-file references. The key is in *reading the output*, not in restricting the input scope.

---

## JSON Output Fields

When running with JSON output, the response is an array of **diagnostic objects**. The relevant fields are:

| Field | Type | Purpose |
|---|---|---|
| `diagnostics[].uri` (or `file`) | `string` | Absolute or workspace-relative path of the file where the error was detected |
| `diagnostics[].severity` | `"error"` \| `"warning"` | Whether this is a hard failure or advisory |
| `diagnostics[].message` | `string` | Human-readable description of the problem |
| `diagnostics[].range.start.line` | `number` | 0-based line number inside the offending file |

### Distinguishing "only my file failed" vs "whole project broken"

1. **Only your file failed** — all diagnostic entries with `severity: "error"` have a `uri` value that resolves to `projects/template/system-model.c4`. No errors reference other source files.

   ```json
   [
     {
       "uri": "projects/template/system-model.c4",
       "severity": "error",
       "message": "Unknown element kind 'servicee'",
       "range": { "start": { "line": 12, "character": 4 } }
     }
   ]
   ```

2. **Whole project broken** — diagnostic entries with `severity: "error"` reference files *other than* `system-model.c4` (e.g. shared specs, view files, other project files). This indicates a cascading failure where your change broke cross-file references or the shared specification is inconsistent.

   ```json
   [
     {
       "uri": "projects/shared/spec-components.c4",
       "severity": "error",
       "message": "Duplicate element identifier 'api'",
       "range": { "start": { "line": 5, "character": 2 } }
     }
   ]
   ```

### Decision rule

```
if all errors[].uri === "projects/template/system-model.c4"
  → only your file has problems
else if any errors[].uri !== "projects/template/system-model.c4"
  → project-wide breakage (check those other files too)
```

A result with **zero error-severity diagnostics** (empty array or only `"warning"` entries) means validation passed cleanly.
