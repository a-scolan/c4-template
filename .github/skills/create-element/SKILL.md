---
name: create-element
description: Create elements with proper naming (PascalCase kinds, camelCase vars), required metadata (technology, description), and correct hierarchy.
---

# Create LikeC4 Element

Use this skill when creating or modifying any LikeC4 element.

**Before creating:** 
1. Read `c4-modeling-process` skill to understand C4 framework and top-to-bottom design (C1 → C2 → C3)
2. **Check shared specification first** - Use `read-project-summary` MCP to list available element kinds
3. Only create new kinds if absolutely necessary (and ask permission first)

## Shared Spec First Principle

**IMPORTANT:** Use existing element kinds from shared spec instead of creating new ones.

### Why Use Shared Spec?
- Consistency across models and projects
- Maintainability - changes apply everywhere
- Visual consistency - same kinds always look the same
- Avoiding proliferation - keep kinds focused and organized

### How to Use Shared Spec
1. Run `read-project-summary` to see available kinds
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

1. **Naming:** Element kind uses `Category_Subtype` PascalCase (e.g., `Container_API`, `Node_VM`)
2. **Variable:** Instance name uses camelCase (e.g., `apiGateway`, `prodVM`)
3. **Technology:** Required for Containers, Components, and Nodes
4. **Description:** Required for ALL elements (explain purpose and responsibilities)
5. **Tags:** 
   - Use model tags (#System, #External, #Service, #Queue) in system-model.c4
   - Use deployment tags (#Production, #Networking, #Monitoring) in deployment.c4
   - Never repeat tags already in the element kind specification
6. **Hierarchy:** Place in correct parent (Containers inside Systems, Components inside Containers)

## Essential Metadata

### Technology Stack

```likec4
model {
  api = Container_API 'REST API' {
    technology 'Node.js, Express'
    description 'Handles business logic and data processing'
  }
  
  service = Component_Service 'User Service' {
    technology 'Java 17, Spring Boot, Hibernate'
    description 'User management and authentication'
  }
}
```

### Rich Descriptions with Markdown

```likec4
model {
  apiGateway = Container_Gateway 'API Gateway' {
    #critical #production
    technology 'Kong'
    
    description """
      Central entry point for all API requests.
      
      **Responsibilities:**
      - Authentication and authorization
      - Rate limiting and request routing
      
      **Availability:** 99.9% SLA
    """
  }
}
```

### External Documentation Links

```likec4
model {
  paymentService = Component_Service 'Payment Service' {
    #pci-compliant #production
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
    #production
    technology 'PostgreSQL 15'
    description 'Primary application database'
    icon tech:postgresql
  }
  
  cache = Container_Cache 'Redis Cache' {
    #production
    technology 'Redis 7'
    description 'Session and data cache'
    icon tech:redis
  }
}
```

Common icon namespaces: `tech:`, `aws:`, `gcp:`, `azure:`

## Tagging Guidelines

### Environment Tags
```likec4
prodAPI = Container_API 'Production API' {
  #production #us-east-1
  technology 'Node.js'
  description 'Production API server'
}
```

### Architectural Tags
```likec4
frontend = Container_WebApp 'Frontend' {
  #presentation #public-facing
  technology 'React'
  description 'User interface'
}

database = Container_Database 'Database' {
  #data #persistent
  technology 'PostgreSQL'
  description 'Data storage'
}
```

### Status and Compliance
```likec4
legacyService = Component_Service 'Legacy Service' {
  #deprecated #migration-pending
  technology 'Java 8'
  description 'Legacy user service'
}

paymentDB = Container_Database 'Payment Data' {
  technology 'PostgreSQL'
  description 'Payment transactions'
  #pci-compliant, #encrypted, #pii
}
```

## Validation Checklist

- [ ] Technology specified for Containers, Components, and Nodes
- [ ] Description provided for ALL elements (explain purpose)
- [ ] Descriptions use Markdown for structure when multi-line
- [ ] Links use HTTPS and descriptive text (not "click here")
- [ ] Icons use valid namespace (tech:, aws:, gcp:, azure:)
- [ ] Tags lowercase, hyphen-separated, match spec declarations
- [ ] Element placed in correct parent hierarchy

## MCP Validation

**Before creating:** Use `read-project-summary` to check declared element kinds and tags  
**After creating:** Use `read-element` to verify metadata completeness  
**For searching:** Use `search-element` to find elements by tag

## Context7 Validation

Use Context7 MCP `query-docs` with library `/likec4/likec4` if uncertain about:
- Element property syntax (technology, description, link, icon)
- Markdown formatting in descriptions
- Icon namespace conventions

## Output

Well-documented elements with complete metadata, proper hierarchy, and consistent naming.
