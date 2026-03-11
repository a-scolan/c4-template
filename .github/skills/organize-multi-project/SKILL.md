---
name: organize-multi-project
description: Use when structuring a LikeC4 workspace with multiple projects sharing specifications, or when creating a new project derived from the template.
---

# Organize Multi-Project Workspace

## Overview

Defines folder structure, configuration, and shared-spec patterns for LikeC4 workspaces containing multiple projects. Each project has its own `likec4.config.json` and includes the shared specification directory. New projects are created from the `projects/template/` starting point.

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
| New project bootstrap | Copy/adapt from `projects/template/` |
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

### Use Template Project

When creating a new project, use `projects/template/` as starting point:

1. **Check for template:** Read `projects/template/likec4.config.json` and `system-*.c4` files
2. **Copy structure:** Replicate file structure and shared includes
3. **Update config:** Change project `name` and `title` in likec4.config.json
4. **Preserve includes:** Keep `"paths": ["../shared"]` for shared specs

**If template not available locally:** Use GitHub MCP `get_file_contents` to retrieve from c4_template repository temporarily:
- `projects/template/likec4.config.json`
- `projects/template/system-model.c4`
- `projects/template/system-views.c4`

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

❌ **Not using the template project** — always copy `projects/template/` as a starting point to preserve the correct config and file structure

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