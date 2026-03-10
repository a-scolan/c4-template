---
name: c4-modeling-process
description: C4 modeling methodology - design system hierarchy top-to-bottom from Context to Components. Use when creating or reviewing architecture diagrams, ensuring C1→C2→C3 progression, or validating model completeness.
---

# C4 Modeling Process

**Core principle:** Design top-to-bottom (C1 → C2 → C3) for clarity and progressive detail.

## Quick Reference

| Level | Focus | Key Question |
|-------|-------|--------------|
| **C1** | System boundary | Who/what interacts? |
| **C2** | Containers (runtime units) | How is it built? |
| **C3** | Components (code groupings) | What's inside? |

**Optional add-ons:** Deployment (where runs), Dynamic (how behaves)

See [REFERENCE.md](REFERENCE.md) for detailed guidance.

## Workflow

```
1. C1 Context
   ├─ Define system boundary
   ├─ Identify actors (users, external systems)
  └─ Create relationships (see `create-relationship` skill)

2. C2 Containers  
   ├─ Break into deployable units
   ├─ Show container relationships
   └─ Document technologies

3. C3 Components (selective)
   ├─ Detail complex containers only
   └─ Show code-level groupings

4. Deployment (optional)
  └─ Model infrastructure (where)

5. Dynamic (optional)
  └─ Document workflows (how)

6. Validate
   └─ Run: npx likec4 validate
```

## Step 1: C1 Context

Define system boundary and external interactions:

```likec4
model {
  mySystem = System 'Product Name' {
    description 'Core business system'
  }
  
  customer = Actor_Person 'Customer' {
    description 'End user'
  }
  
  externalService = System_Existing 'Payment API' {
    #external
    description 'Third-party payment processor'
  }
  
  customer -> mySystem 'Uses'
  mySystem -> externalService 'Processes payments via'
}
```

**Checklist:**
- [ ] System defined with description
- [ ] All actors identified
- [ ] External systems tagged #external
- [ ] C1 view created in `views 'C1'` folder

**CRITICAL:** C1 views must be static (no flows). Temporal sequences belong in `views 'Use Cases'`.

## Step 2: C2 Containers

Break system into runtime boundaries:

```likec4
model {
  mySystem = System 'Product' {
    frontend = Container_Spa 'Web UI' {
      technology 'React'
      description 'User interface'
    }
    
    api = Container_API 'API' {
      technology 'Node.js'
      description 'Business logic'
    }
    
    database = Container_Database 'Database' {
      technology 'PostgreSQL'
      description 'Data persistence'
    }
  }
  
  frontend -[calls]-> api 'HTTP requests'
  api -[reads]-> database 'Queries'
  api -[writes]-> database 'Updates'
}
```

**Container definition:** Runtime boundary - something that must be running for the system to work. Can be deployed independently.

**Not containers:** Classes, modules, folders, layers (those are components or code organization).

**Checklist:**
- [ ] Containers are independently deployable
- [ ] Technologies documented
- [ ] Relationships show sync vs async
- [ ] C2 view created showing all containers

See [REFERENCE.md](REFERENCE.md) for container vs component distinction.

## Step 3: C3 Components

Detail internal structure of complex containers only:

```likec4
model {
  api = Container_API 'API' {
    router = Component_Service 'Router' {
      description 'Request routing'
    }
    auth = Component_Service 'Auth' {
      description 'Authentication logic'
    }
    business = Component_Service 'Business' {
      description 'Domain logic'
    }
  }
  
  router -[uses]-> auth 'Validates'
  router -[uses]-> business 'Delegates'
}
```

**Component definition:** Code-level grouping with well-defined interface. NOT separately deployable.

**Checklist:**
- [ ] Only detail critical/complex containers
- [ ] Components are logical groupings, not classes
- [ ] C3 view shows parent container boundary
- [ ] Neighboring elements included for context

## Deployment Diagrams

Show where software runs:

```likec4
deployment {
  Prod = Node_Environment 'Production' {
    AppTier = Zone 'App Tier (VLAN 101)' {
      ApiVm = Node_Vm 'api-vm' {
        technology 'Docker'
        description '| IP | 10.1.0.10/24 |'
        
        apiApp = Node_App 'API' {
          instanceOf mySystem.api
        }
      }
    }
  }
}
```

Use `model-deployment` skill for detailed infrastructure modeling.

## Dynamic Diagrams

Show runtime behavior for key use cases:

```likec4
views 'Use Cases' {
  dynamic view upload_flow {
    title 'File Upload'
    
    customer -> mySystem.frontend 'Uploads file'
    mySystem.frontend -> mySystem.api 'POST /upload'
    mySystem.api -> mySystem.storage 'Store file'
    mySystem.api -> mySystem.queue 'Queue processing'
  }
}
```

**Place in `views 'Use Cases'`**, never in C1. Requires C2+ elements.

Create 2-5 dynamic diagrams for important workflows only.

Use `create-sequence-view` skill for detailed guidance.

## Validation

Run validation before committing:

```bash
npx likec4 validate
```

**Manual checks:**
- [ ] Every element has description and technology
- [ ] Every relationship has label
- [ ] Every view has title and description
- [ ] Naming consistent (C1/C2/C3 prefixes)

See [CHECKLIST.md](CHECKLIST.md) for complete validation criteria.

## View Organization

**Mandatory structure:**

```likec4
views {
  view index extends c1_context { }  // Required at root
}

views 'C1' {
  view c1_context { }
}

views 'C2' {
  view c2_containers { }
}

views 'C3' {
  view c3_component_name { }
}

views 'Use Cases' {
  dynamic view workflow_name { }
}

views 'Deployment' {
  deployment view environment_name { }
}
```

All views except index must be in category folders.

## Common Anti-Patterns

❌ Bottom-up design (starting with code)
✅ Top-to-bottom (C1 → C2 → C3)

❌ Every class as container
✅ Containers are runtime boundaries

❌ Components are deployable
✅ Only containers are deployable

❌ C3 for every container
✅ C3 only for complex containers

❌ Flow views in C1
✅ Flows belong in 'Use Cases'

See [REFERENCE.md](REFERENCE.md) for detailed anti-pattern explanations.

## Related Skills

Use these skills at each step:

- `create-element` - Create systems, containers, components
- `create-relationship` - Define interactions
- `design-view` - Organize views in subfolders
- `model-deployment` - Infrastructure modeling
- `create-sequence-view` - Dynamic diagrams
- `test-model` - Validation workflow

## Resources

- **C4 Model:** https://c4model.com/
- **LikeC4:** https://likec4.dev/
