Use this single command:

```bash
npx likec4 validate \
  --files projects/template/system-model.c4 projects/template/system-views.c4 \
  --format json \
  --no-layout-drift
```

To confirm both files were actually filtered in JSON output:

1. Check the filtered/validated files list in the JSON (field name may be `files`, `validatedFiles`, or similar).
2. Verify it contains **exactly 2 entries**.
3. Verify those two entries are exactly:
   - `projects/template/system-model.c4`
   - `projects/template/system-views.c4`
4. Also verify diagnostics/issues reference only those two paths (no extra file paths).
