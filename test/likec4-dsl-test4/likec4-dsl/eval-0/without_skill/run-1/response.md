# LikeC4 CLI Syntax & Semantic Validation

## Command

From the repo root, run:

```bash
likec4 check projects/template/system-model.c4
```

If the CLI does not support single-file targeting, the equivalent full-project check is:

```bash
likec4 check
```

To suppress layout output and focus on errors only, add `--no-output` or `--reporter json`:

```bash
likec4 check --reporter json 2>&1
```

## JSON Output Fields

When using `--reporter json`, the output contains an array of diagnostic objects. Key fields:

| Field | Description |
|---|---|
| `file` | Absolute or relative path to the source `.c4` file where the issue was found |
| `severity` | `"error"` \| `"warning"` \| `"info"` |
| `message` | Human-readable description of the syntax or semantic problem |
| `range.start.line` / `range.end.line` | Line numbers within the file |
| `code` | Optional error code identifying the rule violated |

## Distinguishing File-Level vs Project-Level Failures

- **Only your file failed**: All diagnostic entries have `"file"` pointing to `projects/template/system-model.c4`. Other files have no `"error"` severity entries.
- **Whole project broken**: Diagnostics appear across multiple files, or there are errors in shared spec files (e.g. `projects/shared/spec-*.c4`) that cascade into your file.

Filter the JSON output for `severity === "error"` entries and group by `file`. If all errors are isolated to `projects/template/system-model.c4`, only that file is broken.

```bash
likec4 check --reporter json | python -c "
import json, sys
diags = json.load(sys.stdin)
errors = [d for d in diags if d.get('severity') == 'error']
files = set(d['file'] for d in errors)
print('Files with errors:', files)
"
```

> **Note:** LikeC4 validates the whole project graph on every `check` run because elements and relationships can cross file boundaries. A single-file check flag may not exist; what you get is project-wide output that you then filter by `file` field to identify the scope of the failure.
