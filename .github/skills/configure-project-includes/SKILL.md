---
name: configure-project-includes
description: Use when configuring or updating likec4.config.json includes, image aliases, or multi-file project organization (system-model, system-views, deployment, operations).
---

# Manage LikeC4 Project Includes

## Overview

This skill is for **project-local configuration**, not for redesigning the whole workspace. Use it to keep `likec4.config.json` correct, preserve shared specs and image aliases, and split a growing project into a small number of coherent files without breaking imports.

## When to Use

- Adding a new project that needs to reference shared specs
- Splitting a monolithic `.c4` file into focused files (model, views, sequences, deployment)
- Adding or updating image aliases for icon consistency
- Appending a new shared specification path without breaking existing includes

**Do not use** for:
- editing model elements or relationships
- deciding overall multi-project boundaries for the workspace
- rewriting views themselves

For whole-workspace structure, hand off to `organize-multi-project`.

## Core Rule

Treat `likec4.config.json` as a **targeted configuration file**:

- preserve what already works
- add paths instead of replacing them blindly
- keep paths **relative to the project folder**
- keep the shared image alias intact unless you are intentionally migrating icons

## Single vs. Multi-File Organization

### Small Projects (Single File)
For simple systems, one model file works:
```
project/
  system.c4              # All elements, relationships, and views
```

### Growing Projects (Split Progressively)
Do not jump from one file to seven files unless the project actually needs it.

Start with the smallest useful split:

```
project/
  system-model.c4        # Elements + relationships
  system-views.c4        # C1/C2/C3 views + index
```

Then add focused files only when their topic becomes large enough to deserve its own home:

```
project/
  system-model.c4        # Elements and relationships
  system-views.c4        # C1/C2/C3 views + index
  system-sequences.c4    # Optional: dynamic views in 'Use Cases'
  deployment.c4          # Optional: deployment nodes and instanceOf
  deployment-views.c4    # Optional: deployment views
  operations.c4          # Optional: operational topology
  operations-views.c4    # Optional: operations views
```

**Default template baseline in this repo:**

```
project/
  likec4.config.json
  system-model.c4
  system-views.c4
```

Use that baseline first unless the project already has meaningful deployment, operations, or dynamic-view density.

### File Organization Convention

- **Model files:** structural declarations → `system-model.c4`, `deployment.c4`, `operations.c4`
- **View files:** static/deployment visualizations → `system-views.c4`, `deployment-views.c4`, `operations-views.c4`
- **Sequences:** dynamic flows → `system-sequences.c4`
- **Config:** project-level includes and aliases → `likec4.config.json`

### Required View Category Folders (Hard Rule)

Every view MUST be nested inside a category folder using `views 'FolderName'`, **except** the **index** view.

**Index exception (required at root):**
```likec4
views {
  view index extends c1_context { }
}
```

No other views should be placed in the root `views { }` block.

**Required folder names and file placement:**
- **`C1`** → `system-views.c4`
- **`C2`** → `system-views.c4`
- **`C3`** → `system-views.c4`
- **`Use Cases`** → `system-sequences.c4` when dynamic flows deserve extraction
- **`Deployment`** → `deployment-views.c4` when deployment views exist
- **`Operations`** → `operations-views.c4` when operations views exist

## Config Shape to Preserve

The template config in this repo looks like this:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template-project",
  "title": "My Project Title",
  "include": {
    "paths": ["../shared"]
  },
  "imageAliases": {
    "@": "../shared/images/"
  }
}
```

When editing an existing project config, preserve these concepts unless the user explicitly wants a different shared structure:

- `$schema`
- `name`
- `title`
- `include.paths`
- `imageAliases`

## Quick Reference

| Rule | Correct | Wrong |
|------|---------|-------|
| Path format | `"../shared"` | `/absolute/path/shared` |
| Add include | Append to `paths` array | Replace existing paths |
| Image alias key | `"@"` inside `imageAliases` | removing alias or changing key casually |
| Config filename | `likec4.config.json` | any other name |
| Image path | `"../shared/images/"` | missing alias or absolute icon path base |

## Safe Edit Pattern

When a project already has working includes, modify it surgically:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "payments",
  "title": "Payments Architecture",
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

**Meaning:**
- keep existing shared sources
- add the new source
- keep the shared image alias
- avoid unrelated reformatting or reorganization

## Example: New Project from Template

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "my-project",
  "title": "My Project",
  "include": {
    "paths": ["../shared"]
  },
  "imageAliases": {
    "@": "../shared/images/"
  }
}
```

## Handoff Rules

Use this skill when the task is mainly about **how a project config points to shared assets and how files are split inside one project**.

Hand off when the scope becomes larger:

- new workspace or multiple project boundaries → `organize-multi-project`
- element kinds, relationships, or view logic → the corresponding modeling/view skills
- validating that the edited model still works → `test-model`

## Common Mistakes

❌ **Absolute paths** — LikeC4 requires relative paths; use `../shared`, not `/home/user/shared`

❌ **Replacing existing paths** — always append to the `paths` array to preserve current includes

❌ **Dropping the shared image alias** — omitting `"@": "../shared/images/"` breaks icon references across all views

❌ **Exploding the file structure too early** — don’t create deployment/operations/sequence files until the project actually needs them

❌ **Treating this as the multi-project architecture skill** — if the user is deciding project boundaries or adding a second project, use `organize-multi-project`

❌ **Mixing model and views in one file** — for projects larger than a few hundred lines, split into focused files per organization convention above

## Done Criteria

- `likec4.config.json` keeps valid shared includes
- image aliases still resolve shared icons
- paths remain relative to the project folder
- existing includes are preserved unless intentionally removed
- file splitting is progressive and matches actual project complexity
- multi-project concerns are handed off instead of absorbed here
