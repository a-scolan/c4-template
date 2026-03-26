# Eval 4 — Adding `../platform-shared` that redefines image aliases

## The problem

`platform-shared` has its own images and its alias key may conflict with the existing `"@": "../shared/images/"`. Silently overwriting `"@"` would break every existing icon reference in the model.

## How to adjust safely

### `include.paths` — append only

```json
"paths": [
  "../shared",
  "../platform-shared"
]
```

Never remove `"../shared"`. It provides both element specs and the base image set.

### `imageAliases` — introduce a distinct key for the new source

Keep the canonical `"@"` alias pointing to `../shared/images/`. Introduce a new alias key (e.g., `"@platform"`) for images coming from `platform-shared`.

```json
"imageAliases": {
  "@": "../shared/images/",
  "@platform": "../platform-shared/images/"
}
```

## Complete safe result

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "payments",
  "title": "Payments Architecture",
  "include": {
    "paths": [
      "../shared",
      "../platform-shared"
    ]
  },
  "imageAliases": {
    "@": "../shared/images/",
    "@platform": "../platform-shared/images/"
  }
}
```

## Why not overwrite `"@"`?

All existing views use `@icon-name` as the shared icon reference prefix. Changing what `"@"` resolves to would silently reroute every existing icon to the platform folder, potentially breaking or mismapping icons that exist only in `../shared/images/`. The two-key approach avoids any collision.

## Using the new alias in views

New elements or views that need platform icons use `@platform/icon-name`. Existing model files continue using `@/icon-name` unchanged.
