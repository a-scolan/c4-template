# Eval 3 — Adding a second LikeC4 project: is this skill enough?

## Short answer: No — hand off to `organize-multi-project`

This skill (`configure-project-includes`) is **project-local**: it handles `likec4.config.json` edits, include paths, image aliases, and file splitting *within one existing project*.

Adding a second project means deciding workspace-level boundaries, which is explicitly outside the scope of this skill.

## Recommended workflow

1. **Use `organize-multi-project`** to:
   - decide the second project's folder placement in the workspace
   - establish what is shared vs. project-specific
   - create the workspace structure (new folder + initial `likec4.config.json`)

2. **Return to `configure-project-includes`** once the folder exists to:
   - set the correct `include.paths` pointing to shared specs
   - add the correct `imageAliases` for icon resolution
   - split project files progressively if needed

## What `configure-project-includes` handles after handoff

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "second-project",
  "title": "Second Project",
  "include": {
    "paths": ["../shared"]
  },
  "imageAliases": {
    "@": "../shared/images/"
  }
}
```

This skill configures the config correctly once the project exists; it does not decide whether the project should exist or where it fits in the workspace.
