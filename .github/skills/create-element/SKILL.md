---
name: create-element
description: Use when creating or modifying LikeC4 elements (systems, containers, components, nodes) with proper naming conventions, required metadata, and correct C4 hierarchy placement.
---

# Create LikeC4 Element

## Overview

Defines the rules and patterns for declaring LikeC4 elements: naming conventions (PascalCase kinds, camelCase variables), required fields (technology, description), tag usage, icon references, and correct parent-child hierarchy (System → Container → Component).

## When to Use

- Creating a new system, container, component, or deployment node
- Modifying element properties (technology, description, tags, icon)
- Checking whether an existing shared-spec kind fits your need before creating a custom one
- Adding metadata fields used for filtering or automation

**Do not use** to create relationship arrows or design views — use `create-relationship` and `design-view` respectively.

**Before creating:**
1. Read `c4-modeling-process` skill to understand C4 framework and top-to-bottom design (C1 → C2 → C3)
2. **Check shared specification first** - Use LikeC4 MCP `read-project-summary` to list available element kinds
3. Only create new kinds if absolutely necessary (and ask permission first)
4. When adding relationships, follow `create-relationship` skill

**If you need rich descriptions:** Use `write-rich-descriptions` for metadata blocks (system models) or markdown tables (deployment models).

## Quick Reference

| Topic | Rule |
|------|------|
| Kind naming | `Category_Subtype` in PascalCase (`Container_Api`, `Node_Vm`) |
| Variable naming | camelCase (`apiGateway`, `prodUploadVm`) |
| Required fields | `technology` + `description` (where applicable by kind) |
| Tag source | Reuse declared shared-spec tags with exact spelling/case; do not duplicate them in metadata |
| Hierarchy | System → Container → Component; Environment → Zone → VM → App |
| New kind creation | Prefer shared spec first; ask before introducing new kinds |

## Shared Spec First Principle

**IMPORTANT:** Use existing element kinds from shared spec instead of creating new ones.

### Why Use Shared Spec?
- Consistency across models and projects
- Maintainability - changes apply everywhere
- Visual consistency - same kinds always look the same
- Avoiding proliferation - keep kinds focused and organized

### How to Use Shared Spec
1. Run LikeC4 MCP `read-project-summary` to see available kinds
2. Check `spec-*.c4` files in `shared/` folder
3. Use existing kind that matches your need
4. **If no matching kind exists:**
   - Ask user permission first
   - Suggest contributing new kind to shared spec
   - Don't create one-off custom kinds in project-specific files
   - Add to spec so it can be reused

## C4 Design Hierarchy

Always design **top-to-bottom:**
- **C1 Context:** System boundary with external actors and systems
- **C2 Container:** Major deployable components and their relationships  
- **C3 Component:** Internal modules within important containers (optional, for complex containers only)

See `c4-modeling-process` skill for detailed step-by-step guidance.

## Validation Rules

1. **Naming:** Element kind uses `Category_Subtype` PascalCase exactly as declared in shared specs (e.g., `Container_Api`, `Node_Vm`)
2. **Variable:** Instance name uses camelCase (e.g., `apiGateway`, `prodVM`)
3. **Technology:** Required for Containers, Components, and Nodes
4. **Description:** Required for ALL elements (explain purpose and responsibilities)
5. **Tags:** 
  - Reuse declared shared-spec tags only when they add meaning beyond the kind itself
  - Keep the declared spelling/case exactly as-is (for example `#Production`, not `#production`)
  - Never repeat family/type tags already implied by the element kind specification
6. **Metadata:** Optional (only add if you filter/query by the field)
7. **Hierarchy:** Place in correct parent (Containers inside Systems, Components inside Containers)

## Essential Metadata

### Technology Stack

```likec4
model {
  api = Container_Api 'REST API' {
    technology 'Node.js, Express'
    description 'Handles business logic and data processing'
  }
  
  userService = Component 'User Service' {
    technology 'Java 17, Spring Boot, Hibernate'
    description 'User management and authentication'
  }
}
```

### Rich Descriptions with Markdown

```likec4
model {
  ingestionApi = Container_Api 'Ingestion API' {
    technology 'Node.js, Fastify'
    
    description """
      Receives file uploads and starts the ingestion workflow.
      
      **Responsibilities:**
      - Validate upload requests
      - Forward accepted files to downstream processing
      
      **Availability:** 99.9% SLA
    """
  }
}
```

### External Documentation Links

```likec4
model {
  paymentIntegration = Component 'Payment Integration' {
    technology 'Node.js, Stripe SDK'
    description 'Handles payment processing'
    
    link https://docs.stripe.com 'Stripe API Docs'
    link https://github.com/myorg/payment-service 'Source Code'
  }
}
```

### Icons

```likec4
model {
  database = Container_Database 'PostgreSQL' {
    technology 'PostgreSQL 15'
    description 'Primary application database'
    icon tech:postgresql
  }
  
  queue = Container_Queue 'Async Queue' {
    technology 'RabbitMQ'
    description 'Buffers background jobs and asynchronous processing'
    icon tech:rabbitmq
  }
}
```

Common icon namespaces: `tech:`, `aws:`, `gcp:`, `azure:`

## Tagging Guidelines

Prefer tags only when they add queryable operational meaning. The element kind already carries most family/type semantics.

### Deployment / runtime tags
```likec4
prodApiVm = Node_Vm 'Production API VM' {
  #Production #Service
  technology 'Ubuntu 22.04'
  description 'Hosts the production API workload'
}
```

### Backup / recovery tags
```likec4
backupWorker = Node_App 'Backup Worker' {
  #Backup #Recovery
  technology 'BorgBackup'
  description 'Runs scheduled backups and restore checks'
}
```

## Validation Checklist

- [ ] Technology specified for Containers, Components, and Nodes
- [ ] Description provided for ALL elements (explain purpose and responsibilities)
- [ ] Descriptions use Markdown for structure when multi-line
- [ ] Links use HTTPS and descriptive text (not "click here")
- [ ] Icons use valid namespace (tech:, aws:, gcp:, azure:) if adding icons
- [ ] Tags match shared-spec spelling/case exactly when reusing declared tags
- [ ] Element placed in correct parent hierarchy
- [ ] Metadata (optional) — only if you filter/query by those fields

## MCP Validation

**Before creating:** Use LikeC4 MCP `read-project-summary` to check declared element kinds and tags  
**After creating:** Use `read-element` to verify description quality and technology field  
**For searching:** Use `search-element` to find elements by tag

## Context7 Validation

Use Context7 MCP `query-docs` with library `/likec4/likec4` if uncertain about:
- Element property syntax (technology, description, link, icon)
- Markdown formatting in descriptions
- Icon namespace conventions

## Common Mistakes

❌ **Using guessed kind names** — `Container_API`, `Container_Gateway`, `Component_Service`, `Node_VM` are not declared in this repo.

❌ **Using a generic base kind when a shared subtype exists** — prefer `Container_Api` or `Container_Database` over bare `Container` for common application elements.

❌ **camelCase kind, PascalCase variable** — kinds must be `PascalCase_Subtype`; variables must be `camelCase`

❌ **Missing technology on Containers/Components** — `technology` field is required for all non-actor elements

❌ **Description missing** — all elements must have a description explaining their purpose and responsibilities

❌ **Creating one-off custom kinds** — always check shared spec first; contributing to spec ensures consistency across projects

❌ **Placing Containers outside their System** — hierarchy must be: System → Container → Component

## Output

Well-documented elements with complete descriptions, proper hierarchy, and consistent naming. Metadata is optional and minimal.
