Run from repo root:

```
npx likec4 check projects/template/
```

The `check` command validates syntax and semantics for the whole project without rendering or computing layouts, so no layout drift is triggered.

To get machine-readable output, add `--reporter json` if your CLI version supports it:
```
npx likec4 check --reporter json projects/template/
```

JSON fields to scope the failure:
- Each diagnostic object has a `file` (or `uri`) field containing the absolute/relative path of the offending source file.
- If every entry in the `errors` array has `file` pointing only to `projects/template/system-model.c4` → only that file is broken (syntax or local semantic error).
- If any entries reference other files (e.g. shared spec files, other model files) → the project as a whole is broken and the root cause is wider than your edit.
- The top-level `hasErrors` boolean (or a zero vs non-zero exit code) tells you whether any error exists at all; the per-diagnostic `file` field tells you *where*.
