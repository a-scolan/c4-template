Use this single command:

```bash
likec4 validate --json --no-layout --files projects/template/system-model.c4 projects/template/system-views.c4
```

Then confirm filtering in the JSON by checking that the validated file list (or per-file diagnostics entries) contains exactly these two paths and no others.