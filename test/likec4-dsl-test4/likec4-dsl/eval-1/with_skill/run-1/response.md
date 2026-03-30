# Minimal config snippet

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "include": {
    "paths": ["../shared"]
  }
}
```

Place this file at `projects/template/likec4.config.json`.

# How LikeC4 assigns a `.c4` file to a project

LikeC4 uses **nearest-config-file wins**: for any `.c4` file, LikeC4 walks up the directory tree and assigns the file to the project whose config file is closest to it in the hierarchy.

Concretely in this workspace:

| File location | Nearest config | Belongs to |
|---|---|---|
| `projects/template/system-model.c4` | `projects/template/likec4.config.json` | `template` project |
| `projects/shared/spec-global.c4` | none above `projects/shared/` (no config there) | no project on its own |

Because `projects/shared/` has no config file of its own, the shared files are **not** automatically picked up by any project. The `include.paths` option in `projects/template/likec4.config.json` is what explicitly pulls those files into the `template` project — LikeC4 scans `../shared` (relative to the config file) and loads every `.c4` file found there as part of the `template` project.

**Key rule:** if `projects/shared/` were given its own `likec4.config.json`, its `.c4` files would belong to *that* project instead, and including them in `template` via `include.paths` would still work — the included files are loaded into both projects independently. Each project gets its own merged model.
