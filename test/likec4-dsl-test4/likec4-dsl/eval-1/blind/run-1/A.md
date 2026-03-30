# LikeC4 Multi-Project Config with Shared Specs

## Minimal `likec4.config.json` snippet

```json
{
  "name": "template",
  "include": [
    "./**/*.c4",
    "../shared/**/*.c4"
  ]
}
```

Place this file at `projects/template/likec4.config.json`. The `include` array accepts glob patterns relative to the config file location, so `../shared/**/*.c4` pulls in all `.c4` files from the sibling `shared/` directory.

## How LikeC4 assigns `.c4` files to projects

When multiple `likec4.config.json` files exist in the workspace, LikeC4 uses the following rules:

1. **Each config defines its own project.** Every `likec4.config.json` is the root of one project. Files are associated with a project based on that project's `include` globs.

2. **Globs are evaluated relative to the config file.** A path like `../shared/**/*.c4` is resolved from the directory that contains the config, so `projects/template/likec4.config.json` with `../shared/**/*.c4` resolves to `projects/shared/**/*.c4`.

3. **A file can belong to multiple projects.** If `projects/spec-showcase/likec4.config.json` also includes `../shared/**/*.c4`, the shared files are parsed in both projects independently. There is no global deduplication—each project gets its own model scope.

4. **No automatic inheritance.** Files in `projects/shared/` are not automatically visible to other projects; you must explicitly include them via globs in every config that needs them.

5. **Isolation by default.** Elements, kinds, and relationships defined in one project do not leak into another unless the source files are explicitly included.

## Summary

| Config location | `include` entry | Files resolved |
|---|---|---|
| `projects/template/likec4.config.json` | `"./**/*.c4"` | all `.c4` under `projects/template/` |
| `projects/template/likec4.config.json` | `"../shared/**/*.c4"` | all `.c4` under `projects/shared/` |

Both entries together give the `template` project access to its own model files **and** the shared specification definitions.
