---
name: design-view
description: Design views with proper includes/excludes and basic layout. Use for include patterns, tag filtering, and simple rank hints. For advanced styling/navigation, use customize-view.
---

# Design LikeC4 View

Use this skill when creating or modifying visualization views.

## Core Principles

### 1. Always Include Parent/Surrounding Context

**Every view MUST explicitly include the parent/surrounding element for context:**

| View Type | Shows | Must Include |
|-----------|-------|------------------|
| C3 Component | Internal modules | Parent Container |
| C2 Container | System building blocks | Parent System |
| C1 Context | System in landscape | External Systems |
| Deployment VM | VM internals | Parent Zone |
| Deployment Zone | Infrastructure services | Parent Environment |
| Dynamic Sequence | Step-by-step flows | Initiating Actor |

This ensures every view answers: "What is this IN? What surrounds it?"

### 2. Show Neighboring Elements (Focused C2/C3 Views)

**Focused views of containers and components MUST show related/neighboring elements:**
- Include all elements that have relationships WITH the focused element(s)
- Shows incoming relationships: `include -> element.*` (what calls this?)
- Shows outgoing relationships: `include element.*` then `include element.* ->` (what does this call?)
- Provides interaction context: "How does this fit in the larger system?"

This ensures every focused view answers: "What uses this? What does it use?"

### 3. Use Shared Spec for Elements & Styling

**When designing views, always prefer shared specification:**
- Use element kinds defined in `shared/spec-*.c4`
- Use colors defined in `shared/spec-global.c4`
- Don't create custom kinds, colors, or styles in view-specific files
- If something is needed:
  1. Check shared spec first
  2. Ask permission from user
  3. Contribute to shared spec instead
  4. Then use the spec definition

This ensures consistency and maintainability across all views and projects.

### 4. Wire Drill-Down Navigation (navigateTo)

**When you create a new view, also update the parent overview view with a `navigateTo` link** so users can zoom in from the higher-level diagram.

**Rule of thumb (C4):**
- C1 → C2: add `navigateTo` from system context to container view
- C2 → C3: add `navigateTo` from container overview to component view
- Deployment overview → tier/zone details: add `navigateTo` from overview elements

**Example (C2 to C3 drill-down):**
```likec4
view c2_containers {
  include mySystem.*
  include mySystem.webapp with {
    navigateTo c3_webapp
  }
}

view c3_webapp {
  include mySystem.webapp
  include mySystem.webapp.*
}
```

## View Organization Hierarchy

**Hard rule:** Every view MUST be nested inside a category folder using the `views 'FolderName'` syntax, **except** the **index** view.

**Index exception:** The index view **must** live at the root:
```likec4
views {
  view index extends c1_context { }
}
```

Do not place any other views in the root `views { }` block.

**Avoid duplicate category prefixes:** When a view is inside a category folder, **do not** prefix the view title with the same category (e.g., avoid `title 'C1 / System Context'` inside `views 'C1'`). Choose **one**: folder name OR title prefix, not both.

**Allowed categories (must use these exact folder names):**
- `C1` (System Context)
- `C2` (Containers)
- `C3` (Components)
- `Use Cases` (Dynamic/sequence views)
- `Deployment` (Infrastructure views)
- `Operations` (Security/monitoring/DR/CI/CD)

**Example (all views inside folders):**

```likec4
// Root index view (ONLY view allowed at root)
views {
  view index extends c1_context {
    title 'Architecture Overview'
    description 'Navigate to detailed views for deeper exploration'
  }
}

// C1 - System Context
views 'C1' {
  view c1_context { ... }
}

// C2 - Containers
views 'C2' {
  view c2_containers { ... }
}

// C3 - Components
views 'C3' {
  view c3_component1 { ... }
  view c3_component2 { ... }
}

// Use Cases - temporal flows and interactions
views 'Use Cases' {
  dynamic view upload_flow { ... }
  dynamic view retrieval_flow { ... }
  dynamic view data_replication { ... }
}

// Deployment - infrastructure and physical layout
views 'Deployment' {
  deployment view overview { ... }
  deployment view user_access { ... }
  deployment view app_tier { ... }
  deployment view data_tier { ... }
}

// Operations - monitoring, security, disaster recovery
views 'Operations' {
  deployment view security { ... }
  deployment view backup_recovery { ... }
  deployment view cicd { ... }
}
```

### Detailed Subfolder Contents

#### C1 Context (`views 'C1' { }`)
**Purpose:** System boundary with external actors and systems

**Content:**
- Who uses the system?
- External systems it integrates with?
- High-level information flows
- **✓ MUST include system boundary** - Always show what is INSIDE vs. OUTSIDE the system
- **Index View (MANDATORY):** Architecture entry point
  - **✓ MUST extend c1_context** - Inherits system context by default (unless explicitly asked otherwise)
  - **If a C0 landscape view exists, extend that instead** (e.g., `view index extends c0_landscape { }`)
  - **Always include braces** (even if empty) to keep the syntax explicit
  - Typically titled "Architecture Overview" or "[System Name] - Overview"

**Minimal example (with braces):**
```likec4
views {
  view index extends c1_context {
  }
}
```

#### C2 Containers (`views 'C2' { }`)
**Purpose:** System building blocks and their relationships

**Content:**
- Services, databases, message queues, APIs, integration points
- Technology choices
- **✓ MUST include system for container context** - Always show containers WITHIN the system boundary

#### C3 Components (`views 'C3' { }`)
**Purpose:** Deep-dive into specific containers (one view per major container)

**Content:**
- Internal modules/components within a container
- Design patterns and responsibilities
- One dedicated view per major service/container
- **Naming:** View ID should reference the container: `c3_<container_name>` → Title: `<Container Name>`
- Examples: `c3_upload_service` → "Upload Service", `c3_retrieval_service` → "Retrieval Service"
- **✓ MUST include parent container for context** - Always show the container boundary with its components inside

**File:** `system-views.c4`

**Example IDs:** `c1_context`, `c2_container`, `c3_upload_service`, `c3_retrieval_service`, `c3_processing_worker`, `index`

#### Use Cases (`views 'Use Cases' { }`)
**Purpose:** Temporal flows - show how system behaves during important operations

**Content:**
- **Sequence diagrams** (dynamic views) showing step-by-step interactions
- **User workflows:** Happy path, validation, error handling
- **Data flows:** Movement of data through the system
- **Async patterns:** Message processing, notifications, background jobs
- **Disaster recovery:** Failover, replication, recovery procedures
- Titles should be plain (no category prefix) since the folder provides the category
- **✓ MUST include actors initiating flows** - Always show who/what starts the sequence

**File:** `system-sequences.c4`

**Example IDs:** `usecases_upload_flow`, `usecases_retrieval_flow`, `usecases_backup_flow`

#### Deployment (`views 'Deployment' { }`)
**Purpose:** Physical infrastructure - show how system runs in production

**Content:**
- **Network topology:** Zones, VLANs, internet gateways
- **User access:** Browser → CDN → servers → APIs
- **Service tier breakdown:** Separate views for each tier (app, data, processing)
- **VM and container placement:** Where services run
- **Service-to-infrastructure mapping:** Which services use which resources
- **High-level availability:** Multi-node clusters, load balancers
- **✓ MUST include parent zones/environments** - Always show VMs WITHIN their zones, zones WITHIN their environments

**File:** `deployment-views.c4`

**Example IDs:** `user_access`, `overview`, `app_tier`, `proc_tier`, `data_tier`

#### Operations (`views 'Operations' { }`)
**Purpose:** Runtime concerns - monitoring, security, reliability

**Content:**
- **Security & Monitoring:** Monitoring infrastructure, log aggregation, metrics
  - Alert systems and notification channels
  - Intrusion detection and firewalls
- **Backup & Disaster Recovery:** High availability and failover
  - Replication across regions/zones
  - Backup storage and recovery procedures
  - RTO/RPO specifications
- **CI/CD Pipeline:** Build, test, and deployment automation
  - Build agents and artifact storage
  - Test environments and production deployments
  - Rollback and rollforward procedures

**File:** `operations-views.c4`

**Example IDs:** `security`, `backup_recovery`, `cicd`

### File Organization Best Practice

```
project/
  system-model.c4           # ← Elements, containers, components
  system-views.c4           # ← views 'C1'/'C2'/'C3' → architecture hierarchy
  system-sequences.c4       # ← views 'Use Cases' { } → workflows
  deployment.c4             # ← Deployment nodes and VMs
  deployment-views.c4       # ← views 'Deployment' { } → infrastructure
  operations.c4             # ← Operations infrastructure
  operations-views.c4       # ← views 'Operations' { } → monitoring/DR
```

## Including Neighboring Elements (Related by Relationships)

For **focused C2 or C3 views**, always include neighboring elements to show interaction context:

### Syntax for Including Relationships

```likec4
view c2_container {
  // Core focus: the container(s) being analyzed
  include mySystem.uploadService
  
  // What calls this container?
  include -> mySystem.uploadService
  
  // What does this container call?
  include mySystem.uploadService ->
  
  // Include parent for context
  include mySystem
}
```

### Examples of Related Element Inclusion

**Include direct callers (incoming):**
```likec4
// Add all elements that have relationships TO this component
include -> vault.uploadService
```

**Include dependencies (outgoing):**
```likec4
// Add all elements that this component depends on
include vault.uploadService ->
```

**Include related child components:**
```likec4
// Include related nested services/components
include vault.uploadService.*
include vault.minio.*  // What it depends on
```

### Why Show Neighbors?

Without neighboring elements:
- ❌ View shows isolated container/component
- ❌ Unclear how it fits in larger system
- ❌ Missing interaction context

With neighboring elements:
- ✓ View shows focused element + related elements
- ✓ Clear what uses it and what it uses
- ✓ Complete interaction context

---

## Complete Examples from Refactored Project

### C1 Folder: C1 Context View
Shows system boundary and external actors/systems
```likec4
views 'C1' {
  view c1_context {
    title 'Secure Vault System'
    include customer
    include browser
    include vault
    include scanner
    
    rank source { customer }
    rank sink { scanner }
  }
}
```

### C2 Folder: C2 Container View
Shows major components (containers) and their relationships + neighboring elements
```likec4
views 'C2' {
  view c2_container {
    title 'Vault System Internals'
    
    // Focus: system and its containers
    include customer
    include browser
    include vault.*
    include scanner
    
    // Show complete interaction context
    include -> vault.*    // What calls our containers?
    include vault.* ->    // What do our containers call?
    
    rank source { customer }
    rank sink { scanner }
  }
}
```

### C3 Folder: C3 Component Deep-Dives
Shows internal modules within a specific container (one view per major service)
- **Naming:** C3 view ID should reference the container it explains: `c3_<container_name>`
- **Title:** `<Container Name>` (e.g., "Upload Service", "Retrieval Service")
- **Content:** Include the container, its child components, and related external systems + neighboring containers

```likec4
views 'C3' {
  view c3_upload_service {
    title 'Upload Service'
    
    // Focus: container and its components
    include vault.uploadService.*
    
    // Parent container for context
    include vault.uploadService
    
    // Neighboring containers (what interacts with this service)
    include customer
    include browser
    include -> vault.uploadService    // What calls it?
    include vault.uploadService ->    // What does it call?
    
    rank source { customer }
    rank sink { vault.minio }
  }
  
  view c3_retrieval_service {
    title 'Retrieval Service'
    
    // Focus: container and its components
    include vault.retrievalService.*
    include vault.retrievalService
    
    // Neighboring elements
    include customer
    include browser
    include -> vault.retrievalService
    include vault.retrievalService ->
    
    rank source { customer }
    rank sink { vault.minio }
  }
  
  view c3_processing_worker {
    title 'Processing Worker'
    
    // Focus: container and its components
    include vault.worker.*
    include vault.worker
    
    // Neighboring elements
    include -> vault.worker
    include vault.worker ->
    
    rank source { vault.messageQueue }
    rank sink { vault.minio }
  }
}

### Use Cases Subfolder: Upload Workflow Sequence
Shows temporal flow from customer action to final storage
```likec4
views 'Use Cases' {
  dynamic view usecases_upload_flow {
    title 'Upload'
    
    customer -> browser 'Upload file'
    browser -> vault.webServer 'Load SPA (if needed)'
    vault.webServer -> browser 'Serve React SPA'
    browser -> vault.frontend 'SPA loaded in browser'
    vault.frontend -> vault.api.router 'POST /api/upload'
    vault.api.router -> vault.api.auth 'Authenticate'
    vault.api.router -> vault.uploadService.uploadModule 'Route to upload module'
    vault.uploadService.uploadModule -> vault.uploadService.uploadModule 'Validate file (fail-fast)'
    vault.uploadService.uploadModule -> vault.jobs 'Publish FileValidated'
    vault.worker.consumerModule -> vault.jobs 'Consume message'
    vault.worker.orchestratorModule -> vault.worker.scannerModule 'Scan for viruses'
    vault.worker.scannerModule -> scanner 'Check file'
    scanner -> vault.worker.scannerModule 'Clean'
    vault.worker.encryptorModule -> vault.docDB 'Store encryption key'
    vault.worker.minioModule -> vault.minio 'Put encrypted object (primary)'
    vault.minio -> vault.worker.minioModule 'Stored'
    vault.worker.metadataModule -> vault.docDB 'Set READY'
  }
}
```

### Deployment Subfolder: Explicit Element Includes (Best Practice)

**CRITICAL RULE:** Every deployment view MUST explicitly list every deployment element that should appear in the diagram. Never use wildcards (`*` or `**`). Always add comments documenting which elements are shown.

**Why?** Explicit includes make architecture hierarchy obvious, prevent unexpected element bloat, and serve as self-documenting architecture (the view file IS the documentation).

#### Pattern 1: Overview with Zones and All Elements Explicit

```likec4
views 'Deployment' {
  /**
   * Infrastructure Overview
   * Elements explicitly shown:
   * - Zone1: pc1, designer1, print1, printer1
   * - Zone2: pc2, designer2, print2, printer2
   */
  deployment view infrastructure {
    title 'Infrastructure - 2 Postes avec Imprimantes'
    description 'Two identical zones: each with PC, Designer, Print, and USB printer.'
    
    // Zone 1 - List all elements explicitly
    include lanInterne.zone1.posteWindows1
    include lanInterne.zone1.posteWindows1.designerApp1
    include lanInterne.zone1.posteWindows1.printApp1
    include lanInterne.zone1.printer1
    include lanInterne.zone1
    
    // Zone 2 - List all elements explicitly  
    include lanInterne.zone2.posteWindows2
    include lanInterne.zone2.posteWindows2.designerApp2
    include lanInterne.zone2.posteWindows2.printApp2
    include lanInterne.zone2.printer2
    include lanInterne.zone2
    
    // Parent environment for context/flows
    include lanInterne
  }
}
```

#### Pattern 2: Detail View with All Services Explicit

```likec4
views 'Deployment' {
  /**
   * Server Zone Details
   * Elements explicitly shown:
   * - serveur (parent node)
   * - automationService
   * - printServer
   * - templateShare
   * - fileDropShare
   * - eventLog
   */
  deployment view zone_serveur_details {
    title 'Server Node - Services & Storage'
    description 'Inside server: Automation Service, Print Server, SMB shares, Event Log.'
    
    // Explicitly list each service (DO NOT use wildcards)
    include lanInterne.zoneServeur.serveur.automationService
    include lanInterne.zoneServeur.serveur.printServer
    include lanInterne.zoneServeur.serveur.templateShare
    include lanInterne.zoneServeur.serveur.fileDropShare
    include lanInterne.zoneServeur.serveur.eventLog
    
    // Include parent nodes for context
    include lanInterne.zoneServeur.serveur
    include lanInterne.zoneServeur
  }
}
```

**Key principles:**
- **ALWAYS explicit lists**, never wildcards
- **ALWAYS add comments** documenting which elements appear in the view
- **ALWAYS include parent** (zone or environment) for context and relationships
- **ALWAYS document in view comment** the exact list of elements shown
- **Order matters:** Children first, then parent (ensures visibility)

### Deployment Subfolder: Zone-Based Overview with Explicit Includes
Shows infrastructure organized by network zones with explicit zone and elements includes for clarity
```likec4
views 'Deployment' {
  // Overview: Show ALL zones explicitly (hierarchy is clear from nesting)
  deployment view lan_overview {
    title 'Infrastructure - Network Overview'
    description 'Complete infrastructure: client zones, server zones, and devices. Each zone represents a logical network segment with controlled access.'
    
    // Explicitly include each major zone and key elements
    include lanInterne.zoneClients.pc1.app1
    include lanInterne.zoneClients.pc1
    include lanInterne.zoneClients
    
    include lanInterne.zoneServers.server1.service1
    include lanInterne.zoneServers.server1
    include lanInterne.zoneServers
    
    include lanInterne.zoneDevices.device1
    include lanInterne.zoneDevices
    
    // Include the parent zone for context and flows
    include lanInterne
  }

  // Detail view: Zoom into one zone to show internals
  deployment view server_zone_details {
    title 'Server Zone - Internals'
    description 'Detailed view of server zone: VMs, applications, storage, monitoring.'
    
    // Explicitly include internal nodes/services in this zone
    include lanInterne.zoneServers.appServer.webApp
    include lanInterne.zoneServers.appServer.database
    include lanInterne.zoneServers.appServer.monitoring
    
    // Include parent for context
    include lanInterne.zoneServers.appServer
    include lanInterne.zoneServers
  }
}
```

**Key principle:** 
- **ALWAYS explicit** → List every element that should appear in the diagram
- **NEVER use wildcards** → `*` and `**` are forbidden in production deployment views
- **ADD COMMENTS** → Document exactly which elements are shown for maintainability
- **Parent context** → Always include the parent container/zone for navigation and flows
- **Why?** Explicit includes make architecture hierarchy obvious and serve as self-documenting architecture

### Deployment Subfolder: Application Tier Infrastructure
Shows how services are deployed across VMs with tier connectivity
```likec4
views 'Deployment' {
  deployment view app_tier {
    title 'Application Tier'
    description 'Microservices deployed across VM instances with external interactions'
    
    include
      Prod.AppTier.** where tag is #Vm,
      Internet._ ->,
      Prod.Dmz._ ->,
      -> Prod.DataTier._,
      -> Prod.ProcTier._,
  }
}
```

### Operations Subfolder: Security & Monitoring Infrastructure
Shows monitoring systems and how all services are monitored
```likec4
views 'Operations' {
  deployment view security {
    title 'Security & Monitoring'
    description 'Monitoring infrastructure with all monitored systems'
    
    include
      Prod.SecZone.** where tag is #Vm,
      Prod.Dmz.** where tag is #Vm,
      Prod.AppTier.** where tag is #Vm,
      Prod.ProcTier.** where tag is #Vm,
      Prod.DataTier.** where tag is #Vm,
      -> Prod.SecZone.*,
      Prod.SecZone.* ->
  }
}
```

## Advanced Filtering with `where` Clauses

Use `where tag is #Tag` and wildcard patterns to create focused views without listing every element.

### Tag-Based Filtering

Filter by tags to show only specific categories:

```likec4
// Show only VMs (not zones or other nodes)
include Prod.AppTier.** where tag is #Vm

// Show only monitoring infrastructure
include Prod.SecZone.** where tag is #Monitoring

// Show only external systems
include * where tag is #External

// Combine: VMs tagged as production
include Prod.** where tag is #Vm,
       Prod.** where tag is #Production
```

### Wildcard Expansion Patterns

```likec4
// All descendants (recursive)
include Prod.AppTier.**           // Shows Prod.AppTier and everything inside

// Direct children only
include Prod.AppTier.*            // Shows immediate VMs in AppTier

// Directed edges with wildcards
include -> Prod.AppTier.*         // Incoming edges TO AppTier VMs
include Prod.AppTier.* ->         // Outgoing edges FROM AppTier VMs
```

### Complex Filtering Example

Create focused views by combining patterns:

```likec4
deployment view app_tier {
  title 'Application Tier with Dependencies'
  description 'All app tier services with connections to adjacent tiers'
  
  include
    Prod.AppTier,              // The tier container itself
    Prod.AppTier.** where tag is #Vm,  // Only VMs, not zones
    Internet._ ->,             // Incoming from Internet
    Prod.Dmz._ ->,             // Incoming from DMZ
    -> Prod.DataTier._,        // Outgoing to DataTier
    -> Prod.ProcTier._         // Outgoing to ProcTier
}
```

### When to Use Filtering

| Pattern | Use Case |
|---------|----------|
| `include Zone.**` | Show entire zone including all VMs |
| `include Zone.** where tag is #Vm` | Show only VMs, hide nested zones |
| `include -> Zone._` | Incoming dependencies to the zone |
| `include Zone._ ->` | Outgoing from zone to other zones |
| `include * where tag is #External` | All external systems across entire deployment |

## Best Practices

1. **Preview with MCP (RECOMMENDED):** Use LikeC4 MCP `open-view` to preview changes after editing
2. **Organize by type:** Group related views (context, containers, deployments) in subfolders
3. **Scoped includes:** Use `include mySystem.*` (children) or `include mySystem.**` (all descendants)
4. **Directed includes:** Use `include -> mySystem.*` (incoming) or `include mySystem.* ->` (outgoing)
5. **Tag filtering:** Use `where tag is #Tag` to focus views dynamically (requires tier/vm tags)
6. **Avoid over-broad:** Never use `include **` or `include ** -> **` (shows too much noise)
7. **Ordering:** Place `exclude` statements after `include` statements
8. **Maintenance:** Update view tags when adding new infrastructure to keep filters working
9. **Layout hints (LAST RESORT ONLY):** Only add `rank source/sink/same` when autoLayout produces poor results. Let LikeC4's automatic layout handle positioning by default.

## Simple Starter Example

```likec4
views 'C2' {
  view c2_containers {
    title 'Container Overview'
    
    include user
    include mySystem.* where tag is #Service
    include externalSystem
  }
}
```
