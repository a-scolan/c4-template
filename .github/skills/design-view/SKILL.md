---
name: design-view
description: Design views with proper includes/excludes and basic layout. Use for include patterns, tag filtering, and simple rank hints. For advanced styling/navigation, use customize-view. Always include parent context (containers in systems, components in containers, VMs in zones). Show neighboring elements via relationship includes (-> element, element ->). Organize views by category (C1/C2/C3/Use Cases/Deployment/Operations).
---

# Design LikeC4 View

Creates architecture visualization views with proper element inclusion, layout hints, and organization.

## Core Principles Quick Reference

| Principle | Rule | Why |
|-----------|------|-----|
| **🔲 Parent Context** | Always include surroundings | Shows "what is this IN?" |
| **🔗 Neighbors** | Include related elements | Shows "what uses this?" |
| **📦 Shared Spec** | Use `shared/spec-*.c4` | Ensures consistency |
| **🔍 Navigation** | Wire `navigateTo` links | Enables drill-down |
| **📁 Organization** | Nest in category folders | Maintains structure |

## Four Step Workflow

### 1. Choose View Type & Category

**View types:**
- C1 (Context): System boundary with external actors
- C2 (Container): System building blocks (services, APIs, databases)
- C3 (Component): Container internals (modules, classes)
- Use Cases (Dynamic): Temporal flows showing step-by-step interactions
- Deployment: Infrastructure topology (zones, VMs, apps)
- Operations: Security, monitoring, DR, CI/CD

**Category rules:**
- ALL views MUST be in category folders
- ONLY exception: `view index` lives at root
- Use exact folder names: `C1`, `C2`, `C3`, `Use Cases`, `Deployment`, `Operations`

### 2. Include Elements (Parent + Focus + Neighbors)

**Always include three layers:**
```likec4
view c3_uploadService {
  // 1. PARENT: Shows "what is this IN?"
  include vault.uploadService           // Parent container
  
  // 2. FOCUS: Shows "what are we analyzing?"
  include vault.uploadService.*         // All child components
  
  // 3. NEIGHBORS: Shows "what interacts with this?"
  include -> vault.uploadService        // Incoming relationships
  include vault.uploadService ->        // Outgoing relationships
}
```

**Parent context requirement by view type:**

| View Type | Must Include Parent |
|-----------|---------------------|
| C3 Component | Parent container |
| C2 Container | Parent system |
| C1 Context | External systems |
| Deployment VM | Parent zone |
| Deployment Zone | Parent environment |
| Dynamic Sequence | Initiating actor |

### 3. Add Basic Layout (Optional)

**Only when autoLayout produces poor results:**
```likec4
view c2_containers {
  // ... include statements ...
  
  rank source { user }        // Top of diagram
  rank sink { database }      // Bottom of diagram
  rank same { api, cache }    // Horizontal alignment
}
```

**Default:** Let LikeC4's automatic layout handle positioning.

### 4. Wire Navigation (If Creating Detailed View)

**When you create a new detail view, update the parent overview:**
```likec4
// Parent overview (system-views.c4)
views 'C2' {
  view c2_containers {
    include vault.*
    include vault.api with {
      navigateTo c3_api       // ← Add this
    }
  }
}

// New detail view (system-views.c4)
views 'C3' {
  view c3_api {
    title 'API Service'
    include vault.api
    include vault.api.*
    include -> vault.api
    include vault.api ->
  }
}
```

## View Organization Structure

**Mandatory folder nesting (except index):**

```likec4
// Root index ONLY
views {
  view index extends c1_context { }
}

// All other views in folders
views 'C1' {
  view c1_context { ... }
}

views 'C2' {
  view c2_containers { ... }
}

views 'C3' {
  view c3_apiService { ... }
  view c3_workerService { ... }
}

views 'Use Cases' {
  dynamic view uploadFlow { ... }
}

views 'Deployment' {
  deployment view overview { ... }
  deployment view appTier { ... }
}

views 'Operations' {
  deployment view security { ... }
  deployment view cicdPipeline { ... }
}
```

### Category Guidelines

#### C1 Context
**Purpose:** System boundary and external landscape
- ✅ Static relationships: actors, systems, boundaries
- ❌ Flow diagrams: use `views 'Use Cases'` instead
- **Index view:** Must extend `c1_context` (or `c0_landscape` if exists)

```likec4
views 'C1' {
  view c1_context {
    title 'System Context'
    include customer                    // Actor
    include vault                       // Your system
    include externalPaymentGateway      // External system
  }
}

views {
  view index extends c1_context { }     // Inherits c1_context
}
```

#### C2 Container
**Purpose:** System internals (zoom into ONE system's containers)
- ✅ All containers within one system + dependencies
- ❌ All actors from C1 (too broad)

```likec4
views 'C2' {
  view c2_vaultContainers {
    title 'Vault Containers'
    include vault                       // System (parent)
    include vault.*                     // All containers
    include -> vault.*                  // What calls our containers?
    include vault.* ->                  // What do we depend on?
  }
}
```

#### C3 Component
**Purpose:** Container internals (one view per major container)
- **Naming:** `c3_<containerName>` → Title: `<Container Name>`
- **Content:** Container + children + neighbors

```likec4
views 'C3' {
  view c3_uploadService {
    title 'Upload Service'
    include vault.uploadService         // Container (parent)
    include vault.uploadService.*       // Components inside
    include -> vault.uploadService      // Incoming calls
    include vault.uploadService ->      // Outgoing calls
  }
}
```

#### Use Cases (Dynamic)
**Purpose:** Temporal flows showing step-by-step interactions
- **Content:** User workflows, data flows, async patterns, DR procedures
- **Always include:** Actors that initiate flows

```likec4
views 'Use Cases' {
  dynamic view uploadFlow {
    title 'Upload Workflow'
    customer -> browser 'Upload file'
    browser -> vault.api 'POST /upload'
    vault.api -> vault.processor 'Process async'
    vault.processor -> vault.storage 'Store file'
  }
}
```

#### Deployment
**Purpose:** Physical infrastructure topology and architecture
- **List ALL elements explicitly** from environment down to each VM
- **NEVER use wildcards** (e.g., `production.*` or `dmz.**`) in deployment views
- **Include hierarchy:** Environment → Zones → Clusters (optional) → VMs
- **Stop at VM level** (don't drill into app instances unless showing deployment relationships)

**Mandatory inclusion pattern:**
```likec4
views 'Deployment' {
  deployment view overview {
    title 'Infrastructure Overview'
    
    // 1. Always include the environment first
    include production
    
    // 2. Include each zone explicitly
    include production.dmzVlan
    include production.appVlan
    include production.dbVlan
    
    // 3. Include clusters (if any) within zones
    include production.appVlan.webCluster
    include production.dbVlan.redisCluster
    
    // 4. Include EVERY VM individually within each zone/cluster
    include production.dmzVlan.lemonldapVm
    include production.appVlan.webCluster.web01Vm
    include production.appVlan.webCluster.web02Vm
    include production.appVlan.apiVm
    include production.dbVlan.redisCluster.redis01Vm
    include production.dbVlan.redisCluster.redis02Vm
    include production.dbVlan.postgresVm
    
    autoLayout TopBottom
  }
}
```

**Complete hierarchy example:**
```
production (Environment)
├── dmzVlan (Zone)
│   └── lemonldapVm (VM)
├── appVlan (Zone)
│   ├── webCluster (Cluster grouping - optional)
│   │   ├── web01Vm (VM)
│   │   └── web02Vm (VM)
│   └── apiVm (VM - can be standalone)
└── dbVlan (Zone)
    ├── redisCluster (Cluster grouping)
    │   ├── redis01Vm (VM)
    │   └── redis02Vm (VM)
    └── postgresVm (VM)
```

**Why explicit includes?**
- ✅ Ensures all infrastructure is visible and documented
- ✅ Makes dependencies and relationships clear
- ✅ Allows proper VM descriptions and metadata (IP, specs, etc.)
- ❌ Wildcards hide infrastructure complexity and skip important details

**❌ DON'T:**
```likec4
// Too vague - missing VMs
include production.*

// Too deep - drilling into app instances
include production.appVlan.apiVm.appInstance

// Wildcard - hides which VMs exist
include production.appVlan.**
```

**✅ DO:**
```likec4
// Explicit environment
include production

// Explicit zones
include production.appVlan
include production.dbVlan

// Explicit clusters (if used for grouping)
include production.appVlan.webCluster

// Explicit VMs (every single one)
include production.appVlan.webCluster.web01Vm
include production.appVlan.webCluster.web02Vm
include production.appVlan.apiVm
include production.dbVlan.postgresVm
```

**Multiple deployment views strategy:**
- **overview:** All zones + all VMs (complete topology)
- **appTier:** Focus on one zone with all its VMs
- **security:** DMZ zones + firewall rules visualization

#### Operations
**Purpose:** Security, monitoring, DR, CI/CD
- **Security:** Monitoring, logs, alerts, firewalls
- **Backup/DR:** HA, replication, backup storage, RTO/RPO
- **CI/CD:** Build agents, test environments, deployment automation

```likec4
views 'Operations' {
  deployment view security {
    title 'Security & Monitoring'
    include prod.secZone.monitoring
    include prod.secZone.firewall
    include -> prod.secZone.*           // What is monitored?
  }
}
```

## Including Neighbors (Relationship-Based)

**Always show interaction context for focused views:**

```likec4
view c2_apiService {
  // Focus element
  include vault.api
  
  // What calls this? (incoming)
  include -> vault.api
  
  // What does this call? (outgoing)
  include vault.api ->
  
  // Parent for context
  include vault
}
```

**Why include neighbors?**
- ❌ Without: Isolated component, unclear interactions
- ✅ With: Complete context showing usage and dependencies

## Filtering Patterns

### Tag-Based Filtering

```likec4
// Only VMs (not zones)
include prod.appTier.** where tag is #Vm

// Only external systems
include * where tag is #External

// Combine multiple filters
include prod.** where tag is #Vm,
       prod.** where tag is #Production
```

### Wildcard Patterns

```likec4
include vault.*                  // Direct children
include vault.**                 // All descendants (recursive)
include -> vault.api             // Incoming to specific element
include vault.api ->             // Outgoing from specific element
include -> vault.*               // Incoming to any child
include vault.* ->               // Outgoing from any child
```

### Directed Includes (Multi-Tier)

```likec4
deployment view appTier {
  include prod.appTier.**          // All VMs in app tier
  include internet._ ->            // Incoming from internet
  include prod.dmz._ ->            // Incoming from DMZ
  include -> prod.dataTier._       // Outgoing to data tier
}
```

## Deployment View Best Practice: Explicit Includes

**CRITICAL:** Always list deployment elements explicitly (never use wildcards in production):

```likec4
deployment view infrastructure {
  /**
   * Elements shown:
   * - Zone1: pc1, designer1, print1, printer1
   * - Zone2: pc2, designer2, print2, printer2
   */
  
  // Zone 1 - explicit list
  include network.zone1.pc1
  include network.zone1.pc1.designer1
  include network.zone1.pc1.print1
  include network.zone1.printer1
  include network.zone1                // Zone (parent)
  
  // Zone 2 - explicit list  
  include network.zone2.pc2
  include network.zone2.pc2.designer2
  include network.zone2.pc2.print2
  include network.zone2.printer2
  include network.zone2                // Zone (parent)
  
  include network                      // Environment (parent)
}
```

**Why explicit?**
- Self-documenting architecture (the view IS the documentation)
- Prevents unexpected element bloat
- Makes hierarchy obvious

## Basic Examples

### C1 Context View
```likec4
views 'C1' {
  view c1_context {
    title 'System Context'
    include customer
    include vault                      // Your system
    include externalPaymentGateway
    include scanner
    
    rank source { customer }
    rank sink { scanner }
  }
}
```

### C2 Container View
```likec4
views 'C2' {
  view c2_containers {
    title 'System Containers'
    include customer                   // Actor
    include vault                      // System (parent)
    include vault.*                    // All containers
    include scanner                    // External system
    include -> vault.*                 // Incoming relationships
    include vault.* ->                 // Outgoing relationships
    
    rank source { customer }
    rank sink { scanner }
  }
}
```

### C3 Component View
```likec4
views 'C3' {
  view c3_uploadService {
    title 'Upload Service'
    include vault.uploadService        // Container (parent)
    include vault.uploadService.*      // Components
    include customer                   // Actor
    include -> vault.uploadService     // Incoming
    include vault.uploadService ->     // Outgoing
    
    rank source { customer }
  }
}
```

### Dynamic Sequence View
```likec4
views 'Use Cases' {
  dynamic view uploadFlow {
    title 'Upload Workflow'
    
    customer -> browser 'Select file'
    browser -> vault.webServer 'Load SPA'
    vault.webServer -> browser 'Serve React app'
    browser -> vault.api 'POST /upload'
    vault.api -> vault.processor 'Validate file'
    vault.processor -> vault.storage 'Store encrypted'
    vault.storage -> vault.processor 'Confirmation'
    vault.processor -> vault.api 'Success'
    vault.api -> browser 'Upload complete'
  }
}
```

### Deployment View
```likec4
views 'Deployment' {
  deployment view overview {
    title 'Production Infrastructure'
    
    // Explicit includes (not wildcards)
    include production.dmzTier.webVm
    include production.appTier.apiVm
    include production.appTier.workerVm
    include production.dataTier.dbVm
    
    // Include parent zones and environment
    include production.dmzTier
    include production.appTier
    include production.dataTier
    include production
  }
}
```

## Best Practices

1. ✅ **Preview with MCP:** Use LikeC4 MCP `open-view` to preview changes
2. ✅ **Include parent:** Always show surrounding context for hierarchy
3. ✅ **Include neighbors:** Show related elements via `->` and `<-` includes
4. ✅ **Use shared spec:** Reference `shared/spec-*.c4` for kinds/colors/shapes
5. ✅ **Explicit deployment includes:** List all elements, never wildcards
6. ✅ **Tag filtering:** Use `where tag is #Tag` for dynamic filtering
7. ✅ **Wire navigation:** Add `navigateTo` when creating detail views
8. ✅ **Organize by category:** Nest views in proper folders
9. ⚠️ **Layout hints last resort:** Only add `rank` when autoLayout fails
10. ❌ **Avoid over-broad:** Never use `include **` (shows too much)

## Common Patterns Reference

See [PATTERNS.md](PATTERNS.md) for:
- Complete multi-tier deployment examples
- Advanced filtering techniques
- Zone-based organization patterns
- Complex relationship includes
- Tag-based dynamic filtering
