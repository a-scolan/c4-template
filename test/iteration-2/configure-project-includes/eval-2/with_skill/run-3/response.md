# Eval 2 — Adding a new shared source while keeping icons working

## The three edit rules

### Rule 1 — Append, never replace

Add the new path to the existing `paths` array. Do not overwrite the array.

```json
// CORRECT
"paths": [
  "../shared",
  "../platform-shared",
  "../new-common-source"
]

// WRONG — destroys existing includes
"paths": ["../new-common-source"]
```

### Rule 2 — Keep paths relative

Use relative paths from the project folder:

```json
"../new-common-source"    // correct
"/workspace/new-common"   // wrong — absolute path
```

### Rule 3 — Do not touch `imageAliases` unless you need new icons from the added source

The existing `"@": "../shared/images/"` alias must remain unchanged. It is the anchor for every `@`-prefixed icon reference in the model. Removing or overwriting it breaks all icon rendering across all views.

## Result after safe edit

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "my-project",
  "title": "My Project",
  "include": {
    "paths": [
      "../shared",
      "../platform-shared",
      "../new-common-source"
    ]
  },
  "imageAliases": {
    "@": "../shared/images/"
  }
}
```

The `"@"` alias still resolves to `../shared/images/`, so existing icon references continue working unchanged. LikeC4 will also pick up element/relationship/view declarations from `../new-common-source`.
