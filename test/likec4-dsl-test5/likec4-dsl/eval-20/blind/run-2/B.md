Use:

`npx likec4 validate --format json --no-layout-drift projects/template/system-model.c4 projects/template/system-views.c4`

To confirm filtering in JSON, verify that only `projects/template/system-model.c4` and `projects/template/system-views.c4` appear in the reported file paths (for example under diagnostics/issues source paths), and that no other model/view file path is present.# Validate Two Specific Files Without Layout Drift Checks

## Exact Command

```bash
likec4 check --json --no-layout projects/template/system-model.c4 projects/template/system-views.c4
```

### Flags explained

| Flag | Purpose |
|------|---------|
| `--json` | Emit structured JSON output instead of human-readable text |
| `--no-layout` | Skip layout drift checks (no comparison against persisted layout snapshots) |
| `projects/template/system-model.c4` `projects/template/system-views.c4` | Restrict validation to exactly these two files |

---

## How to confirm both files were actually filtered in JSON output

The JSON output contains a top-level `files` (or `checkedFiles`) array listing every file the checker processed. After running the command, inspect that array:

```json
{
  "files": [
    "projects/template/system-model.c4",
    "projects/template/system-views.c4"
  ],
  "errors": [],
  "warnings": []
}
```

**Confirmation steps:**

1. **Count entries** – the `files` array must have exactly **2** entries.
2. **Match paths** – verify both `projects/template/system-model.c4` and `projects/template/system-views.c4` are present and no other `.c4` files appear.
3. **No layout keys** – because `--no-layout` was passed, there should be no `layoutDrift` or `layout` key in the output; if such a key is present the flag was not honoured.

You can automate the check with `jq`:

```bash
likec4 check --json --no-layout \
  projects/template/system-model.c4 \
  projects/template/system-views.c4 \
| jq '{file_count: (.files | length), files: .files, has_layout_drift: has("layoutDrift")}'
```

Expected output:

```json
{
  "file_count": 2,
  "files": [
    "projects/template/system-model.c4",
    "projects/template/system-views.c4"
  ],
  "has_layout_drift": false
}
```

A `file_count` of `2` and `has_layout_drift` of `false` confirm that the filter and the no-layout flag both worked correctly.
