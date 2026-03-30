## Minimal `projects/template/likec4.config.json`

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "include": {
    "paths": ["../shared"]
  }
}
```

This tells LikeC4 to also scan `projects/shared/` for `.c4` files and merge them into the `template` project. The `paths` array takes relative paths from the config file's location.

## How LikeC4 assigns a `.c4` file to a project

LikeC4 uses **nearest-config-file wins** resolution:

- Every `.c4` file is assigned to the project whose config file is in the **closest ancestor directory**.
- If `projects/template/likec4.config.json` and `projects/shared/` both exist, a file at `projects/template/system-model.c4` is **owned by the `template` project** because `projects/template/` is the nearest directory containing a config.
- A file at `projects/shared/spec-components.c4` is owned by whatever config file is closest above it. If `projects/shared/` has no config file of its own, it has no standalone project — its files are only reachable through another project's `include.paths`.

**Consequence for your layout:**

| File path | Owning project |
|---|---|
| `projects/template/system-model.c4` | `template` (config in same dir) |
| `projects/shared/spec-components.c4` | none on its own — included into `template` via `include.paths` |

If `projects/shared/` later gains its own `likec4.config.json`, those files would be assigned to the `shared` project when resolved from that directory, and the `template` project's `include.paths` reference would become a cross-project include of an external project's files.
