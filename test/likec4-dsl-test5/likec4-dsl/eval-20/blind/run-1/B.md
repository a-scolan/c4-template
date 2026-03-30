`likec4 validate --json --no-layout-drift --files projects/template/system-model.c4 projects/template/system-views.c4`

To confirm both files were actually filtered, inspect the JSON and verify the file-filter field (for example `files`/`validatedFiles`) contains exactly these two paths and nothing else (count = 2), then confirm all reported diagnostics reference only those two files.# Validating Two Specific Files Without Layout Drift Checks

## Exact Command

```sh
likec4 check --format json --no-layout projects/template/system-model.c4 projects/template/system-views.c4
```

Or, if using `npx`:

```sh
npx likec4 check --format json --no-layout projects/template/system-model.c4 projects/template/system-views.c4
```

- `--format json` (or `-f json`) emits machine-readable JSON output instead of the default human-readable report.
- `--no-layout` skips layout drift validation, so only structural/DSL errors are reported.
- The two positional file arguments restrict processing to exactly those two files.

## How to Confirm Both Files Were Filtered in JSON Output

In the JSON output, look for a top-level `files` array (or a `checkedFiles` / `sources` field, depending on the CLI version). Each entry corresponds to one file that was actually processed. For example:

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

**Verification steps:**

1. Pipe the output to a file and inspect it:
   ```sh
   likec4 check --format json --no-layout \
     projects/template/system-model.c4 \
     projects/template/system-views.c4 > result.json
   ```

2. Check the `files` array contains exactly two entries:
   ```sh
   # On Linux/macOS
   cat result.json | jq '.files | length'   # should print 2
   cat result.json | jq '.files'            # should list only the two paths

   # On Windows (PowerShell)
   Get-Content result.json | ConvertFrom-Json | Select-Object -ExpandProperty files
   ```

3. Confirm no other `.c4` files appear in the `files` list — if so, the file filter was applied correctly.

> **Note:** If the CLI reports a `sources` or `diagnostics` array keyed by file path instead of a flat `files` list, verify that only the two paths appear as keys in that object.
