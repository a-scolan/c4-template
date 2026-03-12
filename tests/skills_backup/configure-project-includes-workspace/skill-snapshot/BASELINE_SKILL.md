---
name: configure-project-includes
description: Use when configuring or updating likec4.config.json includes, image aliases, or multi-file project organization (system-model, system-views, deployment, operations).
---

# Manage LikeC4 Project Includes

## Overview

Controls which specification files and image aliases a LikeC4 project can access. Ensures relative path correctness, preserves existing configuration, and supports multi-file organization strategies.

## When to Use

- Adding a new project that needs to reference shared specs
- Splitting a monolithic `.c4` file into focused files (model, views, sequences, deployment)
- Adding or updating image aliases for icon consistency
- Appending a new shared specification path without breaking existing includes

**Do not use** for editing model elements or view structure — only for project-level configuration (`likec4.config.json`).

## Single vs. Multi-File Organization

### Small Projects (Single File)
For simple systems, one model file works:
```
project/
  system.c4              # All elements, relationships, and views
```

### Large Projects (Multi-File Recommended)
For complex systems, split into focused files:
```
project/
  system-model.c4        # ← Elements and relationships only
  system-views.c4        # ← Architectural views (C1, C2, C3)
  system-sequences.c4    # ← Use case workflows (dynamic views)
  deployment.c4          # ← Deployment definition (infrastructure)
  deployment-views.c4    # ← Deployment visualizations
  operations.c4          # ← Operations infrastructure (monitoring, backup)
  operations-views.c4    # ← Operations visualizations
```

**Benefits:**
- **Collaboration:** Multiple developers edit different files without conflicts
- **Maintainability:** 150-200 line files are easier to navigate than 2000-line files
- **Clarity:** File names indicate content type and purpose
- **Scaling:** Easy to add new model files as system grows

### File Organization Convention

- **Model files:** Define structure → `system-model.c4`, `deployment.c4`, `operations.c4`
- **View files:** Define visualizations → `system-views.c4`, `deployment-views.c4`, `operations-views.c4`
- **Sequences:** Temporal flows → `system-sequences.c4` (separate from system-views)
- **Config:** Project settings → `likec4.config.json`

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
- **`Use Cases`** → `system-sequences.c4`
- **`Deployment`** → `deployment-views.c4`
- **`Operations`** → `operations-views.c4`

## Quick Reference

| Rule | Correct | Wrong |
|------|---------|-------|
| Path format | `"../shared"` | `/absolute/path/shared` |
| Add include | Append to `paths` array | Replace existing paths |
| Image alias key | `"@"` | any other key |
| Config filename | `likec4.config.json` | any other name |

## Example

```json
{
  "name": "my-project",
  "title": "My Project",
  "include": {
    "paths": ["../shared", "../common"]
  },
  "imageAliases": {
    "@": "../shared/images"
  }
}
```

## Common Mistakes

❌ **Absolute paths** — LikeC4 requires relative paths; use `../shared`, not `/home/user/shared`

❌ **Replacing existing paths** — always append to the `paths` array to preserve current includes

❌ **Missing image alias** — omitting `"@": "../shared/images"` breaks icon references across all views

❌ **Mixing model and views in one file** — for projects larger than a few hundred lines, split into focused files per organization convention above