---
name: design-view
description: Use when creating or updating architecture views with proper element inclusion, parent context, neighbor relationships, and category folder organization (C1/C2/C3/Use Cases/Deployment/Operations).
---

# Design LikeC4 View

## Overview

Creates architecture visualization views with correct element inclusion patterns: always show the parent boundary, the focused elements, and their neighbors. Views must live in named category folders (except the root index view). For advanced styling and navigation, use `customize-view` after this skill.

## When to Use

- Creating a new C1/C2/C3, Use Cases, Deployment, or Operations view
- Deciding which elements (parent + focus + neighbors) to include
- Organizing views into the correct category folders
- Suggesting optional layout tweaks only when the preview really needs them

**Do not use** for sequence/dynamic flows — use `create-sequence-view`. For styling, layout control, or navigateTo links — use `customize-view`.

## Quick Reference

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
  include corePlatform.uploadService    // Parent container
  
  // 2. FOCUS: Shows "what are we analyzing?"
  include corePlatform.uploadService.*  // All child components
  
  // 3. NEIGHBORS: Shows "what interacts with this?"
  include -> corePlatform.uploadService // Incoming relationships
  include corePlatform.uploadService -> // Outgoing relationships
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

### 3. Add Basic Layout (Optional and Minimal)

Start with no `rank` hints.

**Only when autoLayout produces poor results:**
```likec4
view c2_containers {
  // ... include statements ...

  // Optional: choose a direction only if the preview clearly benefits from it
  autoLayout TopBottom

  // Optional: anchor the initiating actor if preview still drifts
  rank source { user }
}
```

**Default:** Let LikeC4's automatic layout handle positioning.

**Rule of thumb:** one obvious anchor is usually enough. If you feel you need several `rank` directives, the include set or view scope probably needs adjustment instead.

`autoLayout LeftRight` is also optional, not a default recommendation. Use it when the user explicitly prefers left-to-right reading or when the view is clearly easier to scan that way.

### 4. Wire Navigation (If Creating Detailed View)

**When you create a new detail view, update the parent overview:**
```likec4
// Parent overview (system-views.c4)
views 'C2' {
  view c2_containers {
    include corePlatform.*
    include corePlatform.api with {
      navigateTo c3_api       // ← Add this
    }
  }
}

// New detail view (system-views.c4)
views 'C3' {
  view c3_api {
    title 'API Service'
    include corePlatform.api
    include corePlatform.api.*
    include -> corePlatform.api
    include corePlatform.api ->
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
    include corePlatform                // Your system
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
  view c2_platformContainers {
    title 'Core Platform Containers'
    include corePlatform                // System (parent)
    include corePlatform.*              // All containers
    include -> corePlatform.*           // What calls our containers?
    include corePlatform.* ->           // What do we depend on?
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
    include corePlatform.uploadService  // Container (parent)
    include corePlatform.uploadService.* // Components inside
    include -> corePlatform.uploadService // Incoming calls
    include corePlatform.uploadService -> // Outgoing calls
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
    browser -> corePlatform.api 'POST /upload'
    corePlatform.api -> corePlatform.processingService 'Process async'
    corePlatform.processingService -> corePlatform.objectStorage 'Store file'
  }
}
```

#### Deployment
**Purpose:** Physical infrastructure topology and architecture
- **List ALL elements explicitly** from environment down to each VM
- **NEVER use wildcards** (e.g., `production.*` or `dmz.**`) in deployment views
- **Include hierarchy:** Environment → Zones → Clusters (optional) → VMs
- **Stop at VM level by default**; if you include app instances, use them to show placement or an infra-specific exception, not to redraw inherited application relationships

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
  include corePlatform.api
  
  // What calls this? (incoming)
  include -> corePlatform.api
  
  // What does this call? (outgoing)
  include corePlatform.api ->
  
  // Parent for context
  include corePlatform
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
include corePlatform.*           // Direct children
include corePlatform.**          // All descendants (recursive)
include -> corePlatform.api      // Incoming to specific element
include corePlatform.api ->      // Outgoing from specific element
include -> corePlatform.*        // Incoming to any child
include corePlatform.* ->        // Outgoing from any child
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
    include corePlatform               // Your system
    include externalPaymentGateway
    include scanner
  }
}
```

### C2 Container View
```likec4
views 'C2' {
  view c2_containers {
    title 'System Containers'
    include customer                   // Actor
    include corePlatform               // System (parent)
    include corePlatform.*             // All containers
    include scanner                    // External system
    include -> corePlatform.*          // Incoming relationships
    include corePlatform.* ->          // Outgoing relationships
  }
}
```

### C3 Component View
```likec4
views 'C3' {
  view c3_uploadService {
    title 'Upload Service'
    include corePlatform.uploadService // Container (parent)
    include corePlatform.uploadService.* // Components
    include customer                   // Actor
    include -> corePlatform.uploadService // Incoming
    include corePlatform.uploadService -> // Outgoing
  }
}
```

### Dynamic Sequence View
```likec4
views 'Use Cases' {
  dynamic view uploadFlow {
    title 'Upload Workflow'
    
    customer -> browser 'Select file'
    browser -> corePlatform.webServer 'Load SPA'
    corePlatform.webServer -> browser 'Serve React app'
    browser -> corePlatform.api 'POST /upload'
    corePlatform.api -> corePlatform.processingService 'Validate file'
    corePlatform.processingService -> corePlatform.objectStorage 'Store encrypted'
    corePlatform.objectStorage -> corePlatform.processingService 'Confirmation'
    corePlatform.processingService -> corePlatform.api 'Success'
    corePlatform.api -> browser 'Upload complete'
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

## Common Mistakes

❌ **Missing parent element** — never show containers without their parent system, or components without their parent container

❌ **No neighbors** — always include `-> element` and `element ->` to show what interacts with the focus element

❌ **Wildcards in deployment views** — always list every VM explicitly; `include production.*` skips important details

❌ **Redrawing app traffic in deployment views** — keep `HTTPS`, `HTTP/8080`, `AMQP`, `LDAP`, etc. on system-model relationships and let deployment views inherit them via `instanceOf`

❌ **View outside category folder** — every view except `view index` must be inside a `views 'FolderName'` block

❌ **Dynamic view in C1 folder** — sequence/temporal flows belong in `views 'Use Cases'`, not in structural folders

❌ **Duplicate title prefix** — if inside `views 'C2'`, don’t start title with “C2 /”; use folder scope OR title prefix, not both

## Best Practices

1. ✅ **Preview with MCP:** Use LikeC4 MCP `open-view` to preview changes
2. ✅ **Include parent:** Always show surrounding context for hierarchy
3. ✅ **Include neighbors:** Show related elements via `->` and `<-` includes
4. ✅ **Use shared spec:** Reference `shared/spec-*.c4` for kinds/colors/shapes
5. ✅ **Explicit deployment includes:** List all elements, never wildcards
6. ✅ **Keep deployment edges rare:** prefer inherited logical relationships over manual deployment edges
7. ✅ **Tag filtering:** Use `where tag is #Tag` for dynamic filtering
8. ✅ **Wire navigation:** Add `navigateTo` when creating detail views
9. ✅ **Organize by category:** Nest views in proper folders
10. ⚠️ **Layout hints last resort:** Only add a tiny number of `rank` hints when `autoLayout` still reads badly; obvious anchors such as users are the usual exception
11. ❌ **Avoid over-broad:** Never use `include **` (shows too much)

## Common Patterns Reference

See [PATTERNS.md](PATTERNS.md) for:
- Complete multi-tier deployment examples
- Advanced filtering techniques
- Zone-based organization patterns
- Complex relationship includes
- Tag-based dynamic filtering
