# LLM Instructions for LikeC4 Project Manipulation

This document provides comprehensive guidance for Large Language Models (LLMs) like GitHub Copilot when working with LikeC4 architecture documentation projects. Follow these instructions to maintain consistency, correctness, and adherence to best practices.

---

## Context Gathering Strategy

When working with a LikeC4 project, gather context in this order:

### 1. Read Configuration First
- **File**: `likec4.config.json`
- **Extract**: Project name, title, included paths, image aliases
- **Purpose**: Understand project scope and dependencies

### Project include (config)
- Includes in `likec4.config.json` are **project-level imports**. Keep them relative to the config file (no absolute paths).
- Default template uses `"include": { "paths": ["../shared"] }` to pull shared specs; adjust only if your shared specs live elsewhere.
- Always keep `imageAliases` aligned (e.g., `"@": "../shared/images"`) so icons resolve consistently.
- If you add more shared packs, append to `paths` rather than replacing existing shared specs.

### 2. Read Shared Specifications
- **Location**: `projects/shared/spec-*.c4` files
- **Critical files**:
  - `spec-global.c4` - Colors, tags, core relationship kinds
  - `spec-context.c4` - Actor and System kinds
  - `spec-containers.c4` - Container kinds (30+ types)
  - `spec-components.c4` - Component kinds
  - `spec-deployment.c4` - Deployment node/zone kinds, infrastructure relationships
- **Purpose**: Understand available element kinds, relationship types, tags, and styling

### 3. Examine Model Files
- **Files**: `system-model.c4`, `deployment.c4`, `operations.c4`
- **Extract**: Existing elements, naming patterns, relationship usage
- **Purpose**: Understand current architecture and conventions

### 4. Study View Files
- **Files**: `system-views.c4`, `deployment-views.c4`, `system-sequences.c4`
- **Extract**: Filtering patterns, layout hints, view structure
- **Purpose**: Understand visualization strategies

---

## Include Syntax (Do / Don't)

Use precise include predicates to avoid over-broad diagrams:

- **Scoped vs unscoped `*`:** In unscoped views, `include *` adds only top-level elements; in `view of mySystem { include * }` it adds that element, its children, and related nodes.
- **Targeted wildcards:** Prefer `include mySystem.*` (children) or `include mySystem.**` (all descendants) instead of `include **`.
- **Directed includes:**
  - Incoming: `include -> mySystem.*` pulls elements that have relationships into visible nodes.
  - Outgoing: `include mySystem.* ->` pulls elements that visible nodes connect to.
  - Specific pair: `include customer -> cloud.*` adds both sides and their relationship.
- **Ordering matters:** `exclude` applies after earlier `include` clauses; place excludes last.
- **Avoid:** `include **` or `include ** -> **` (too broad) and untyped relationships.


## MCP Tools for LikeC4 Development

When available, leverage Model Context Protocol (MCP) servers to enhance your understanding and implementation:

### LikeC4 MCP Server

**Purpose**: Query and navigate LikeC4 models programmatically

**When to use**:
- Understanding existing project structure without reading all files
- Finding relationships between elements
- Searching for specific elements across projects
- Validating element references before making changes
- Opening views to preview diagrams

**Key capabilities**:
- `list-projects` - Discover all LikeC4 projects in workspace
- `read-project-summary` - Get complete project overview (elements, views, specifications)
- `search-element` - Find elements by id, title, kind, tags, or metadata
- `read-element` - Get full element details including relationships and deployed instances
- `read-view` - Get view structure (nodes, edges, filters)
- `find-relationships` - Discover direct and indirect relationships between two elements
- `open-view` - Preview a specific view in the editor

**Best practices**:
1. Use `list-projects` or `search-element` first to identify the correct project
2. Use `read-project-summary` to understand available element kinds and tags
3. Use `find-relationships` before adding new relationships to avoid duplicates
4. Use `search-element` to verify element IDs before referencing them

### Context7 MCP Server

**Purpose**: Access up-to-date LikeC4 documentation and syntax references

**When to use**:
- Checking correct syntax for specific LikeC4 features
- Understanding relationship types and their usage
- Learning about view filtering patterns
- Validating icon references and styling options
- Troubleshooting error messages

**How to use**:
1. Resolve library ID: Use `resolve-library-id` with query "LikeC4 DSL syntax documentation" and libraryName "likec4"
2. Query documentation: Use `query-docs` with the resolved library ID and specific questions like:
   - "How to define deployment nodes in LikeC4?"
   - "What are valid relationship kinds in LikeC4?"
   - "How to use wildcards in view includes?"
   - "Syntax for dynamic sequence views"
   - "How to use instanceOf in deployment?"

**Best practices**:
1. Use Context7 for syntax validation before implementing new features
2. Query for specific topics rather than general questions
3. Limit to 3 queries per question to avoid redundancy
4. Cross-reference Context7 answers with local shared specs for project-specific conventions

**Example workflow**:
```
1. User asks: "Add a message queue for async processing"
2. Use LikeC4 MCP → read-project-summary → Get available Container kinds
3. See Container_Queue is available in shared specs
4. Use Context7 MCP → query-docs → "How to model async relationships in LikeC4?"
5. Implement with correct syntax: api -[async]-> queue 'Publishes jobs'
6. Use LikeC4 MCP → find-relationships → Verify no duplicate relationships exist
7. Use LikeC4 MCP → open-view → Preview the updated view
```

---

## Critical Validation Rules

Apply these validation rules to EVERY element and relationship you create or modify:

### ✅ Naming Conventions

**MUST use PascalCase with Category_Subtype pattern:**

```likec4
✅ Actor_Person
✅ System_Existing
✅ Container_Api
✅ Node_Vm
✅ Zone_Vlan

❌ actor_person          (lowercase)
❌ ActorPerson           (no separator)
❌ actor-person          (kebab-case)
❌ ACTOR_PERSON          (screaming snake case)
```

**Exception**: Instance names (variables) use camelCase:
```likec4
✅ mySystem = System_Existing 'My System'
✅ apiGateway = Container_Api 'API Gateway'
```

### ✅ Typed Relationships

**ALL static relationships MUST have explicit relationship kinds:**

```likec4
// Model relationships
✅ api -[calls]-> service 'Invokes'
✅ api -[reads]-> database 'Queries'
✅ worker -[async]-> queue 'Consumes'
✅ api -[writes]-> storage 'Saves'
✅ user -[uses]-> system 'Interacts with'

❌ api -> service 'Invokes'                    // Missing kind
❌ api -[invokes]-> service                    // Invalid kind (not defined)

// Deployment relationships
✅ vm1 -[https]-> vm2 'API calls'
✅ app -[tcp]-> database 'Connects'
✅ service -[amqp]-> queue 'Publishes'

❌ vm1 -> vm2 'Connects'                       // Missing kind
```

**Available relationship kinds** (from `spec-global.c4` and `spec-deployment.c4`):
- Model: `calls`, `async`, `reads`, `writes`, `uses`
- Deployment: `http`, `https`, `tcp`, `nfs`, `amqp`, `sql`, `redis`, `smtp`, `ldap`, `oidc_saml`

### ✅ Required Metadata

**Every element MUST have:**

```likec4
element = ElementKind 'Title' {
  #Tag                                 // ✅ Optional semantic tags (first line after brace)
  technology 'Tech stack'              // ✅ Required for Containers, Components, Nodes
  description 'What it does'           // ✅ Required for ALL elements
}
```

**Tag scope rules:**
- **Model files** (system-model.c4): Use tags from spec-global.c4, spec-context.c4, spec-containers.c4, spec-components.c4 (#System, #External, #Internal, #Legacy, #Cloud, #Saas, #Queue, #Security)
- **Deployment files** (deployment.c4): Use tags from spec-deployment.c4 (#Production, #Development, #Networking, #SharedInfra, #Service, #Monitoring, #Deployment, #Async, #Persistence, etc.)
- ❌ Never use deployment tags (#Service, #Production, #Monitoring) in model files
- ❌ Never use model element tags (#System, #Container, #Actor) in deployment files
- ❌ Never repeat tags already defined in the element kind specification (e.g., `Container_Api` already has `#Container` and `#Api`, don't add them again)
```

**Every relationship MUST have a label:**

```likec4
✅ source -[kind]-> target 'Descriptive label'
✅ source -[kind]-> target 'Label' {
     description 'Additional details'
   }

❌ source -[kind]-> target                     // Missing label
```

### ✅ Fully Qualified Names (FQN)

**Use dots for nested element references:**

```likec4
model {
  mySystem = System_Existing 'System' {
    api = Container_Api 'API'
    database = Container_Database 'DB'
  }
  
  // ✅ Correct: Use FQN in relationships
  mySystem.api -[reads]-> mySystem.database 'Queries'
  
  // ❌ Wrong: Cannot reference just 'api' outside the system block
  api -[reads]-> database
}
```

### ✅ Deployment InstanceOf

**Deployed apps MUST link to model containers:**

```likec4
deployment {
  Prod = Node_Environment 'Production' {
    ApiVm = Node_Vm 'prod-api-vm' {
      apiApp = Node_App 'API App' {
        instanceOf mySystem.api        // ✅ Links to model
      }
    }
  }
}

❌ instanceOf api                      // Must use FQN
❌ instanceOf mySystem                 // Must point to Container, not System
```

---

## Anti-Patterns to Avoid

### ❌ Return Relationships

**Responses are implicit - NEVER create reverse relationships:**

```likec4
✅ client -[calls]-> server 'Requests data'

❌ client -[calls]-> server 'Requests data'
   server -[calls]-> client 'Returns response'    // Wrong: implicit
```

### ❌ Over-Broad Wildcard Includes

**Use scoped wildcards, not global:**

```likec4
view bad_view {
  include ** -> **                     // ❌ Too broad, shows everything
}

view good_view {
  include mySystem.*                   // ✅ Scoped to system
  include user -> mySystem.*           // ✅ Specific relationships
}
```

### ❌ Untyped Elements

**Never use generic kinds when specific ones exist:**

```likec4
❌ api = Container 'API'               // Generic
✅ api = Container_Api 'API'           // Specific

❌ db = Container 'Database'           // Generic
✅ db = Container_Database 'Database'  // Specific
```

### ❌ Missing Technology for Containers

**Containers MUST specify technology:**

```likec4
❌ api = Container_Api 'API' {
     description 'API service'         // Missing technology
   }

✅ api = Container_Api 'API' {
     technology 'Node.js, Express'     // ✅ Required
     description 'API service'
   }
```

### ❌ Port Syntax Errors in Deployment

**Use correct port notation:**

```likec4
// Deployment relationship port descriptions
✅ "any -> 443"                        // Ephemeral source -> target
✅ "8080 -> 8080"                      // Specific source -> target

❌ "443"                               // Missing source
❌ "-> 443"                            // Missing source (use "any")
❌ "port 443"                          // Wrong format
```

---

## Task-Specific Guidance

### Adding a New Element

**Checklist:**
1. Choose correct element kind from shared specs (Actor_*, System_*, Container_*, Component_*, Node_*, Zone_*)
2. Use PascalCase for kind, camelCase for variable name
3. Include `description` (required for all)
4. Include `technology` (required for Containers, Components, Nodes)
5. Add semantic tags (`#Service`, `#External`, `#Infrastructure`, etc.)
6. Place in correct hierarchy (Actors at top level, Containers inside Systems, Components inside Containers)

**Example:**
```likec4
model {
  mySystem = System_Existing 'My System' {
    
    // ✅ Complete element definition
    newService = Container_Api 'New Service' {
      technology 'Python, FastAPI'
      description 'Handles specific business logic'
    }
    // Note: Container_Api already has #Container and #Api tags from spec
  }
}
```

### Adding a Relationship

**Checklist:**
1. Use FQN for source and target
2. Choose typed relationship kind (`calls`, `reads`, `writes`, `async`, `uses` for model; `http`, `https`, `tcp`, etc. for deployment)
3. Add descriptive label
4. Optionally add `description` block for details

**Example:**
```likec4
// ✅ Complete relationship
mySystem.api -[calls]-> mySystem.newService 'Delegates processing' {
  description 'POST /api/process with JSON payload'
}
```

### Creating a View

**Checklist:**
1. Use descriptive view ID (e.g., `c1_context`, `c2_containers`, `deployment_production`)
2. Add clear `title`
3. Use scoped includes (`mySystem.*` not `**`)
4. Add `rank source` for top elements (actors)
5. Add `rank sink` for bottom elements (databases, external systems)
6. Use `where tag is #Tag` for filtering when helpful

**Example:**
```likec4
view c2_services {
  title 'C2 / Services'
  
  include user
  include mySystem.* where tag is #Service
  include mySystem.database
  
  rank source { user }
  rank sink { mySystem.database }
}
```

### Adding Dynamic Sequence

**Checklist:**
1. Use `dynamic view` with descriptive ID
2. Add clear `title` describing the use case
3. Use `->` (not `-[kind]->`) for sequence steps
4. Add descriptive labels for each interaction
5. Show step-by-step flow from user action to system response

**Example:**
```likec4
dynamic view sequence_user_action {
  title 'Use Cases / User Action'
  
  user -> mySystem.webapp 'Initiates action'
  mySystem.webapp -> mySystem.api 'POST /api/action'
  mySystem.api -> mySystem.database 'Store data'
  mySystem.api -> mySystem.queue 'Queue background job'
}
```

### Modifying Deployment

**Checklist:**
1. Use nested hierarchy: `Node_Environment` > `Zone` > `Node_Vm` > `Node_App`
2. Deployment elements use PascalCase for variable names (e.g., `ProdApiVm`)
3. Use `instanceOf` to link `Node_App` to model `Container`
4. Deployment relationships use infrastructure kinds (`https`, `tcp`, etc.)
5. Add port descriptions: `"any -> 443"` or `"8080 -> 8080"`

**Example:**
```likec4
deployment {
  Prod = Node_Environment 'Production' {
    #Production
    
    AppTier = Zone 'Application Tier (VLAN 200)' {
      #Networking
      
      ApiVm = Node_Vm 'prod-api-vm' {
        technology 'Ubuntu 22.04, 8 vCPU, 16GB RAM'
        description 'API service host'
        
        ApiApp = Node_App 'API Application' {
          instanceOf mySystem.api           // ✅ Links to model
        }
      }
    }
  }
}

// Deployment relationships
Prod.AppTier.ApiVm -[https]-> Prod.DataTier.DbVm 'Database queries' {
  description "any -> 5432"
}
```

---

## Common Patterns

### Pattern: External System Integration

```likec4
// 1. Define external system
externalService = System_External 'Third-Party Service' {
  technology 'REST API'
  description 'External service description'
  #External
}

// 2. Add relationship
mySystem.api -[calls]-> externalService 'Integrates with' {
  description 'HTTPS REST calls with OAuth 2.0'
}

// 3. Include in views
view c1_context {
  include mySystem, externalService
  rank sink { externalService }
}
```

### Pattern: Async Processing

```likec4
// 1. Define queue
queue = Container_Queue 'Message Queue' {
  technology 'RabbitMQ'
  description 'Async job queue'
}

// 2. Producer relationship
api -[async]-> queue 'Publishes jobs'

// 3. Consumer relationship
worker -[async]-> queue 'Consumes jobs'
```

### Pattern: Multi-Tier Architecture

```likec4
model {
  mySystem = System_Existing 'System' {
    // Presentation tier
    webapp = Container_WebApp 'Web App' {
      technology 'React'
      description 'User interface'
      #Service
    }
    
    // Application tier
    api = Container_Api 'API' {
      technology 'Node.js'
      description 'Business logic'
      #Service
    }
    
    // Data tier
    database = Container_Database 'Database' {
      technology 'PostgreSQL'
      description 'Data persistence'
    }
  }
  
  // Tier relationships
  webapp -[calls]-> api 'API requests'
  api -[reads]-> database 'Queries'
  api -[writes]-> database 'Updates'
}
```

---

## Workflow for Modifying a Project

### Step 1: Understand Current State
```
OPTION A - Using MCP Tools (Recommended):
Use LikeC4 MCP → read-project-summary → Get complete project overview
Use LikeC4 MCP → search-element → Find relevant elements
Use Context7 MCP → query-docs → Check syntax for features you'll use

OPTION B - Reading Files Directly:
Read likec4.config.json → Understand project scope
Read projects/shared/spec-*.c4 → Know available element kinds
Read system-model.c4 → See existing architecture
Read system-views.c4 → Understand current visualizations
```

### Step 2: Plan Changes
```
Identify what needs to be added/modified
Check if element kinds exist (via MCP read-project-summary or shared specs)
Use Context7 MCP to verify correct syntax for new features
Plan relationship types and labels
Decide which views need updates
Use LikeC4 MCP find-relationships to check for existing connections
```

### Step 3: Implement Changes
```
Add/modify elements in model files
Add/modify relationships with typed kinds
Update views to include new elements
Use Context7 MCP if unsure about specific syntax
```

### Step 4: Validate
```
✅ All elements use PascalCase kinds
✅ All relationships have explicit kinds
✅ All elements have descriptions
✅ Containers have technology
✅ Relationships have labels
✅ FQN used for nested references
✅ Views use scoped wildcards
✅ No return relationships
✅ (Optional) Use LikeC4 MCP → open-view to preview changes
```

---

## Quick Reference: Available Element Kinds

From `projects/shared/` specifications:

**Actors** (C1): `Actor_Person`, `Actor_Staff`, `Actor_Admin`

**Systems** (C1): `System_Existing`, `System_New`, `System_Legacy`, `System_External`

**Containers** (C2): `Container_Api`, `Container_WebApp`, `Container_Database`, `Container_Queue`, `Container_Cache`, `Container_WebServer`, `Container_LoadBalancer`, `Container_Storage`, `Container_FileStore`, `Container_Search`, `Container_Monitor`, `Container_Logger`, `Container_Worker`, `Container_Scheduler`, `Container_Proxy`, `Container_Gateway`, `Container_Service`, `Container_Batch`, `Container_Streaming`, `Container_Analytics`, `Container_Ml`, `Container_Mobile`, `Container_Desktop`, `Container_Plugin`, `Container_Library`, `Container_Framework`, `Container_Runtime`, `Container_Os`, `Container_Browser`

**Components** (C3): `Component`

**Deployment Zones**: `Zone`, `Zone_Internet`, `Zone_Vlan`, `Zone_Lan`

**Deployment Nodes**: `Node_Environment`, `Node_Vm`, `Node_Server`, `Node_App`, `Node_Container`, `Node_Pod`, `Node_Cluster`

**Infrastructure**: `Infra_F5`, `Infra_Firewall`, `Infra_Router`, `Infra_Switch`, `Infra_Vpn`

**Relationship Kinds - Model**: `calls`, `async`, `reads`, `writes`, `uses`

**Relationship Kinds - Deployment**: `http`, `https`, `tcp`, `nfs`, `amqp`, `sql`, `redis`, `smtp`, `ldap`, `oidc_saml`

---

## Error Messages and Solutions

### Error: "Element not found"
**Cause**: Using short name instead of FQN  
**Solution**: Use fully qualified name (e.g., `mySystem.api` not `api`)

### Error: "Unknown element kind"
**Cause**: Using generic or invalid kind  
**Solution**: Check `projects/shared/spec-*.c4` for valid kinds

### Error: "Invalid relationship kind"
**Cause**: Using undefined relationship type  
**Solution**: Use `calls`, `async`, `reads`, `writes`, `uses` (model) or `http`, `https`, `tcp`, etc. (deployment)

### Error: Diagram shows unexpected elements
**Cause**: Over-broad wildcard includes  
**Solution**: Use scoped wildcards (`mySystem.*` not `**`)

### Error: "instanceOf target not found"
**Cause**: Referencing non-existent or wrong element  
**Solution**: Ensure target is a Container in the model, use FQN

---

## Summary Checklist

When working with LikeC4 projects, always:

- ✅ Read `likec4.config.json` first
- ✅ Check `projects/shared/spec-*.c4` for available kinds
- ✅ Use PascalCase for element kinds
- ✅ Use camelCase for variable names
- ✅ Add typed relationship kinds (never bare `->`)
- ✅ Include `description` for all elements
- ✅ Include `technology` for Containers, Components, Nodes
- ✅ Add descriptive labels to all relationships
- ✅ Use FQN for nested elements
- ✅ Use scoped wildcards in views
- ✅ Add `rank` hints for layout
- ✅ Link deployment apps with `instanceOf`
- ❌ Never create return relationships
- ❌ Never use generic element kinds when specific ones exist
- ❌ Never use untyped relationships

**Follow these instructions to maintain consistency and correctness in all LikeC4 projects.**
