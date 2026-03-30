# LikeC4 CLI Validation Command

## Command to run

From the repo root, run syntax and semantic validation (no layout) with:

```bash
likec4 check projects/template/system-model.c4
```

If the CLI does not accept a single-file argument, use the project-scoped check:

```bash
likec4 check projects/template
```

The `check` command performs parse and semantic validation only — it does not compute or emit layout, so there is no risk of layout drift.

## Interpreting the JSON output

When the command is invoked with `--output json` (or `--format json` depending on the CLI version), the result structure includes:

| Field | Meaning |
|---|---|
| `errors` | Array of diagnostic objects. Each entry has a `uri` (or `file`) field pointing to the source file, a `message`, and a `severity`. |
| `errors[].uri` | The file path where the error was found. If this matches `projects/template/system-model.c4`, the issue is local to your file. If it points to another file (e.g. a shared spec), the project-level model is broken independently of your edit. |
| `valid` (or `ok`) | Top-level boolean. `true` means the whole project parsed and validated cleanly. `false` does **not** tell you where the fault is — you must inspect `errors[].uri` to distinguish a local vs. project-wide failure. |

### Distinguishing local vs. project-wide failure

- **Only your file failed**: All entries in `errors` have a `uri` that resolves to `projects/template/system-model.c4`.
- **Project is broken independently**: At least one entry in `errors` has a `uri` pointing to a file you did not touch (e.g. `projects/shared/*.c4` or another model file).
- **Both**: Errors appear under multiple files including yours.

> Note: exact field names (`errors`, `uri`, `valid`) may vary slightly across LikeC4 CLI versions. Always check the CLI's `--help` output or changelog if the fields differ.
