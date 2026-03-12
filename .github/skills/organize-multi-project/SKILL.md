---
name: organize-multi-project
description: Use when structuring a LikeC4 workspace with multiple project folders that share specs, assets, or conventions, or when bootstrapping a new project from a minimal baseline.
---

# Organize Multi-Project Workspace

## Overview

Defines folder structure, shared-spec patterns, and project boundaries for LikeC4 workspaces containing multiple projects. Each project owns its own `likec4.config.json` plus local model/view files, while shared definitions stay in a shared area.

Start new projects from a **minimal baseline** (`likec4.config.json` + model file + views file), not by treating an example project as the canonical source of truth. If a starter project exists locally, use it only as a scaffold and remove its example-specific content immediately.

## When to Use

- Initializing a new LikeC4 workspace with several architectural domains
- Adding a new project to an existing multi-project workspace
- Deciding how to split a growing single-project workspace into domain-scoped projects
- Understanding how cross-project references and shared external systems work

**Tip:** Use `configure-project-includes` when updating include paths or image aliases.

## Quick Reference

| Decision | Recommended Choice |
|---------|---------------------|
| Shared kinds/tags | Keep in `projects/shared/spec-*.c4` |
| Project boundaries | One domain/team/layer per project folder |
| Config ownership | Each project owns its `likec4.config.json` |
| New project bootstrap | Start from a minimal baseline: config + model + views |
| Cross-project dependencies | Keep explicit, minimal, and documented |

## Multi-Project Structure

Organize workspace by domain, team, or architectural layer:

```
workspace/
├── projects/
│   ├── shared/                    # Shared specifications
│   │   ├── spec-global.c4
│   │   ├── spec-context.c4
│   │   ├── spec-containers.c4
│   │   └── images/
│   ├── backend-services/          # Project 1
│   │   ├── likec4.config.json
│   │   ├── system-model.c4
│   │   └── system-views.c4
│   ├── frontend-apps/             # Project 2
│   │   ├── likec4.config.json
│   │   ├── apps-model.c4
│   │   └── apps-views.c4
│   └── infrastructure/            # Project 3
│       ├── likec4.config.json
│       ├── deployment.c4
│       └── deployment-views.c4
```

## Project Configuration

Each project needs `likec4.config.json` with shared includes:

**Tip:** Use `configure-project-includes` when updating include paths or image aliases.

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "backend-services",
  "title": "Backend Services Architecture",
  "include": {
    "paths": ["../shared"]
  },
  "imageAlias": {
    "tech": "https://icons.terrastruct.com/tech/",
    "gcp": "https://icons.terrastruct.com/gcp/"
  }
}
```

## Shared Specifications Pattern

Define reusable element kinds and relationship types:

**shared/spec-global.c4**
```likec4
specification {
  // Colors
  color primary
  color secondary
  
  // Sizes
  size small
  size medium
  size large
  
  // Global tags
  tag deprecated
  tag experimental
  tag production
}
```

**shared/spec-containers.c4**
```likec4
specification {
  element Container_WebApp {
    style {
      shape browser
      color primary
    }
  }
  
  element Container_API {
    style {
      shape rectangle
      color secondary
    }
  }
  
  element Container_Database {
    style {
      shape cylinder
      color muted
    }
  }
}
```

## Project-Specific Models

Reference shared specs and define project elements:

**backend-services/system-model.c4**
```likec4
model {
  // Uses Container_API from shared spec
  backendSystem = System_Backend 'Backend System' {
    api = Container_API 'REST API' {
      technology 'Node.js, Express'
    }
    
    database = Container_Database 'User DB' {
      technology 'PostgreSQL'
    }
    
    api -[reads]-> database 'queries'
  }
}
```

## Cross-Project References

When projects need to reference each other:

**Option 1: Shared External Systems**

Define external systems in shared specs:

```likec4
// shared/external-systems.c4
model {
  externalAuth = System_External 'Auth0' {
    #external
  }
}
```

Projects include shared directory and reference:

```likec4
// backend-services/system-model.c4
model {
  api -> externalAuth 'authenticates via'
}
```

**Option 2: Separate External Project**

Create dedicated external systems project:

```
projects/
├── shared/
├── externals/              # External systems project
│   ├── likec4.config.json
│   ├── external-systems.c4
│   └── external-views.c4
├── backend-services/
└── frontend-apps/
```

## Creating New Projects

### Start from a Baseline, Not an Oracle

When creating a new project:

1. **Identify the shared surface** — where shared specs and shared images live
2. **Create local config** — one `likec4.config.json` for the new project
3. **Create the minimum useful files** — usually `system-model.c4` and `system-views.c4`
4. **Wire shared includes** — keep relative paths to the shared specification directory
5. **Expand only when needed** — add sequence, deployment, or operations files when the project actually grows into them

If your workspace already has a starter project, use it only as a scaffold:
- keep the reusable config concepts
- remove example-specific names and model content
- do not treat the example project as the definition of what every project must look like

### Project Organization

Let users define their own structure based on needs:
- Business domains (payments, inventory, customer)
- Architecture layers (frontend, backend, infrastructure)
- Team ownership (team-web, team-mobile, team-platform)
- Any other organizational pattern

## Common Mistakes

❌ **Project-specific models in shared specs** — `projects/shared/` must only contain reusable definitions; never put project elements (systems, containers) there

❌ **Absolute paths in config** — all `include.paths` must be relative (`../shared`), never absolute

❌ **Circular project dependencies** — project A includes project B which includes project A; restructure so shared content lives in `shared/`

❌ **Missing or inconsistent image aliases** — all projects should use the same `"@": "../shared/images"` alias to keep icon references consistent

❌ **Copying an example project verbatim** — examples can seed a baseline, but they should not leak example names, systems, or views into new projects

## Validation Checklist

- [ ] Each project has `likec4.config.json`
- [ ] All projects include shared specifications via relative paths
- [ ] Shared specs contain only reusable definitions (no project-specific models)
- [ ] Project names are unique and descriptive
- [ ] Image aliases consistent across projects
- [ ] No circular dependencies between projects
- [ ] External system references clearly marked with #external tag

## MCP Validation

Use LikeC4 MCP tools:
1. **list-projects** to see all projects in workspace
2. **read-project-summary** for each project to verify structure
3. **search-element** across projects to find cross-references

## Context7 Validation

Use Context7 MCP `query-docs` with library `/likec4/likec4` to verify:
- Multi-project configuration syntax
- Relative path conventions for includes
- Project naming and structure best practices

## Output

Well-organized multi-project workspace with clear separation of concerns, reusable specifications, and maintainable cross-project references.