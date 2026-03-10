# design-view Patterns Reference

Complete examples and advanced filtering patterns for LikeC4 views.

## Complete Project Examples

### C1 Context View
Shows system boundary and external actors/systems.

```likec4
views 'C1' {
  view c1_context {
    title 'Secure Vault System'
    description 'Complete system context showing actors, vault system, and external integrations'
    
    include customer
    include browser
    include vault                        // Your system
    include scanner                      // External virus scanner
    include externalPaymentGateway       // External payment API
    
    rank source { customer }
    rank sink { scanner, externalPaymentGateway }
  }
}

// Index view MUST extend c1_context (inherits elements)
views {
  view index extends c1_context {
    title 'Architecture Overview'
    description 'Navigate to detailed views for deeper exploration'
  }
}
```

**Key principles:**
- ✅ Static relationships only (who connects to what)
- ❌ No flow diagrams (those go in `views 'Use Cases'`)
- Must include system boundary (what's INSIDE vs. OUTSIDE)

### C2 Container View with Neighbors
Shows major components and their complete interaction context.

```likec4
views 'C2' {
  view c2_containers {
    title 'Vault System Internals'
    description 'All containers within vault system with external dependencies'
    
    // Actors and external systems
    include customer
    include browser
    include scanner
    include externalPaymentGateway
    
    // System and all containers
    include vault                        // System (parent)
    include vault.*                      // All containers
    
    // Complete interaction context
    include -> vault.*                   // What calls our containers?
    include vault.* ->                   // What do our containers call?
    
    rank source { customer }
    rank sink { scanner, externalPaymentGateway }
  }
}
```

**Why include neighbors?**
- Shows complete interaction context
- Reveals incoming dependencies (`-> vault.*`)
- Reveals outgoing dependencies (`vault.* ->`)
- Answers "how does this fit in the larger system?"

### C2 Focused Workflow View
Shows specific subset of containers for a focused workflow.

```likec4
views 'C2' {
  view c2_deploymentFlow {
    title 'Deployment Processing'
    description 'How deployment packages flow through vault containers'
    
    // Focus: specific containers involved in deployment
    include orchestrator.deployer        // External orchestration
    include vault.api                    // Entry point
    include vault.processor              // Processing logic
    include vault.storage                // Final storage
    
    // Show the relationships
    include orchestrator.deployer -> vault.api
    include vault.api -> vault.processor
    include vault.processor -> vault.storage
    
    rank source { orchestrator.deployer }
    rank sink { vault.storage }
  }
}
```

**When to create focused C2 views:**
- Show specific workflows (deployment, runtime, backup)
- Highlight subset of containers for documentation
- Create simpler views for presentations

### C3 Component Deep-Dive Views
One view per major container showing internal modules.

```likec4
views 'C3' {
  // Upload service internals
  view c3_uploadService {
    title 'Upload Service'
    description 'Internal modules handling file uploads'
    
    // Parent container for context
    include vault.uploadService
    
    // All components inside
    include vault.uploadService.*
    
    // External actors and systems
    include customer
    include browser
    
    // Complete interaction context
    include -> vault.uploadService       // What calls this service?
    include vault.uploadService ->       // What does this service call?
    
    rank source { customer }
    rank sink { vault.storage }
  }
  
  // Retrieval service internals
  view c3_retrievalService {
    title 'Retrieval Service'
    description 'Internal modules handling file retrieval and decryption'
    
    include vault.retrievalService
    include vault.retrievalService.*
    
    include customer
    include browser
    
    include -> vault.retrievalService
    include vault.retrievalService ->
    
    rank source { customer }
    rank sink { vault.storage }
  }
  
  // Processing worker internals
  view c3_processingWorker {
    title 'Processing Worker'
    description 'Background worker modules for async processing'
    
    include vault.worker
    include vault.worker.*
    
    include -> vault.worker
    include vault.worker ->
    
    rank source { vault.messageQueue }
    rank sink { vault.storage }
  }
}
```

**Naming convention:**
- View ID: `c3_<containerName>` (e.g., `c3_uploadService`)
- Title: `<Container Name>` (e.g., "Upload Service")

### Dynamic Sequence View (Complete Workflow)
Shows temporal flow from customer action to final storage.

```likec4
views 'Use Cases' {
  dynamic view uploadFlow {
    title 'Upload Workflow'
    description 'Complete file upload flow from browser to encrypted storage'
    
    // User interaction
    customer -> browser 'Upload file'
    browser -> vault.webServer 'Load SPA (if needed)'
    vault.webServer -> browser 'Serve React SPA'
    browser -> vault.frontend 'SPA loaded in browser'
    
    // API entry point
    vault.frontend -> vault.api.router 'POST /api/upload'
    vault.api.router -> vault.api.auth 'Authenticate user'
    vault.api.router -> vault.uploadService.uploadModule 'Route to upload'
    
    // Validation
    vault.uploadService.uploadModule -> vault.uploadService.uploadModule 'Validate file (fail-fast)'
    
    // Async processing
    vault.uploadService.uploadModule -> vault.jobs 'Publish FileValidated event'
    vault.worker.consumerModule -> vault.jobs 'Consume message'
    
    // Virus scan
    vault.worker.orchestratorModule -> vault.worker.scannerModule 'Scan for viruses'
    vault.worker.scannerModule -> scanner 'Check file'
    scanner -> vault.worker.scannerModule 'Clean result'
    
    // Encryption and storage
    vault.worker.encryptorModule -> vault.docDB 'Store encryption key'
    vault.worker.minioModule -> vault.storage 'Put encrypted object'
    vault.storage -> vault.worker.minioModule 'Stored confirmation'
    
    // Finalization
    vault.worker.metadataModule -> vault.docDB 'Set status READY'
  }
}
```

**Key principles:**
- Plain arrows with descriptive labels (no relationship kinds)
- Show complete end-to-end flow
- Include all intermediate steps
- Always include initiating actor

### Deployment View with Explicit Includes
Zone-based infrastructure organized by network tiers.

```likec4
views 'Deployment' {
  /**
   * Infrastructure Overview
   * Shows all zones and key VMs explicitly listed
   * Elements: dmzTier (webVm, lbVm), appTier (apiVm, workerVm), dataTier (dbVm, cacheVm)
   */
  deployment view overview {
    title 'Production Infrastructure'
    description 'Complete production deployment across DMZ, App, and Data tiers'
    
    // DMZ Tier - explicit includes
    include production.dmzTier.webVm
    include production.dmzTier.lbVm
    include production.dmzTier                 // Zone (parent)
    
    // App Tier - explicit includes
    include production.appTier.apiVm
    include production.appTier.workerVm
    include production.appTier                 // Zone (parent)
    
    // Data Tier - explicit includes
    include production.dataTier.dbVm
    include production.dataTier.cacheVm
    include production.dataTier                // Zone (parent)
    
    // Environment (parent)
    include production
  }
}
```

**CRITICAL RULES:**
- ✅ ALWAYS explicit lists (never wildcards in production)
- ✅ ALWAYS include parent zones for context
- ✅ ALWAYS stop at VM level (not app instances)
- ✅ ALWAYS add comments documenting elements shown

### Deployment View Detail (Zone Internals)
Zoom into one zone to show internal services.

```likec4
views 'Deployment' {
  /**
   * Application Tier Details
   * Shows all services running on app tier VMs
   * Elements: apiVm (webApp, authService), workerVm (processor, scheduler)
   */
  deployment view appTierDetails {
    title 'Application Tier - Services'
    description 'Detailed view of app tier: API and worker services'
    
    // API VM services (explicit)
    include production.appTier.apiVm.webApp
    include production.appTier.apiVm.authService
    include production.appTier.apiVm          // VM (parent)
    
    // Worker VM services (explicit)
    include production.appTier.workerVm.processor
    include production.appTier.workerVm.scheduler
    include production.appTier.workerVm       // VM (parent)
    
    // Zone and environment (parents)
    include production.appTier
    include production
  }
}
```

**Pattern:**
- Document exact elements in comment block
- List each service explicitly (no wildcards)
- Include parent VM, zone, environment
- Order: children first, then parents

### Deployment View with Multi-Tier Connectivity
Shows how tiers connect to each other.

```likec4
views 'Deployment' {
  deployment view appTierConnectivity {
    title 'Application Tier - Connectivity'
    description 'App tier VMs with external interactions: incoming from DMZ, outgoing to data/processing tiers'
    
    // App tier VMs (explicit)
    include production.appTier.apiVm
    include production.appTier.workerVm
    include production.appTier
    
    // Directed includes: show tier-to-tier relationships
    include internet._ ->                     // Incoming from internet
    include production.dmzTier._ ->           // Incoming from DMZ
    include -> production.dataTier._          // Outgoing to data tier
    include -> production.processingTier._    // Outgoing to processing tier
    
    include production
  }
}
```

**Directed include patterns:**
- `internet._ ->` — All relationships FROM internet
- `production.dmzTier._ ->` — All relationships FROM dmzTier
- `-> production.dataTier._` — All relationships TO dataTier

### Operations View: Security & Monitoring
Shows monitoring infrastructure and what it monitors.

```likec4
views 'Operations' {
  /**
   * Security & Monitoring Infrastructure
   * Shows: secZone (monitoring, logging, alerts) and all monitored tiers
   */
  deployment view security {
    title 'Security & Monitoring'
    description 'Monitoring infrastructure observing all production tiers'
    
    // Security zone VMs (explicit)
    include production.secZone.monitoringVm
    include production.secZone.loggingVm
    include production.secZone.alertVm
    include production.secZone
    
    // All monitored VMs (explicit per tier)
    include production.dmzTier.webVm
    include production.dmzTier.lbVm
    include production.dmzTier
    
    include production.appTier.apiVm
    include production.appTier.workerVm
    include production.appTier
    
    include production.dataTier.dbVm
    include production.dataTier.cacheVm
    include production.dataTier
    
    // Relationships to/from security zone
    include -> production.secZone.*           // What feeds the security zone?
    include production.secZone.* ->           // What does security zone monitor?
    
    include production
  }
}
```

## Advanced Filtering Techniques

### Tag-Based Dynamic Filtering

**Filter by element type:**
```likec4
// Only VMs (exclude zones and environments)
include production.appTier.** where tag is #Vm

// Only monitoring infrastructure
include production.** where tag is #Monitoring

// Only external systems
include * where tag is #External

// Only services (not infrastructure)
include vault.** where tag is #Service
```

**Combine multiple tag filters:**
```likec4
deployment view productionVms {
  include
    production.** where tag is #Vm,          // All VMs
    production.** where tag is #Production   // Tagged as production
}
```

### Wildcard Expansion Patterns

**Recursive vs. direct children:**
```likec4
include vault.*                    // Direct children only
include vault.**                   // All descendants (recursive)
```

**Pattern breakdown:**
```likec4
// Given hierarchy: system.container.component
include system                     // ONLY the system element
include system.*                   // System + all containers (children)
include system.**                  // System + containers + components (all descendants)
```

**Directed includes with wildcards:**
```likec4
// Incoming relationships
include -> vault.uploadService     // To specific element
include -> vault.*                 // To any child of vault

// Outgoing relationships
include vault.uploadService ->     // From specific element
include vault.* ->                 // From any child of vault
```

### Complex Multi-Pattern Views

**Show app tier with all connections:**
```likec4
deployment view appTierComplete {
  title 'Application Tier - Complete Context'
  
  include
    production.appTier,                       // The tier itself
    production.appTier.** where tag is #Vm,   // All VMs (not zones)
    internet._ ->,                            // Incoming from internet
    production.dmzTier._ ->,                  // Incoming from DMZ
    -> production.dataTier._,                 // Outgoing to data tier
    -> production.processingTier._            // Outgoing to processing tier
}
```

**Show external dependencies:**
```likec4
view c2_externalDependencies {
  title 'External System Dependencies'
  
  include
    vault,                                    // Your system
    vault.*,                                  // Your containers
    * where tag is #External,                 // All external systems
    vault.* -> * where tag is #External       // Only outgoing to external
}
```

### Zone-Based Organization Pattern

**Overview with all zones explicit:**
```likec4
views 'Deployment' {
  /**
   * Network Topology Overview
   * Elements: clientZone (pc1, pc2), serverZone (appServer, dbServer), deviceZone (printer, scanner)
   */
  deployment view networkOverview {
    title 'Network Topology'
    description 'Complete infrastructure organized by network zones'
    
    // Client zone (explicit)
    include network.clientZone.pc1
    include network.clientZone.pc1.browserApp
    include network.clientZone.pc2
    include network.clientZone.pc2.browserApp
    include network.clientZone                    // Zone (parent)
    
    // Server zone (explicit)
    include network.serverZone.appServer
    include network.serverZone.appServer.webService
    include network.serverZone.appServer.apiService
    include network.serverZone.dbServer
    include network.serverZone.dbServer.database
    include network.serverZone                    // Zone (parent)
    
    // Device zone (explicit)
    include network.deviceZone.printer
    include network.deviceZone.scanner
    include network.deviceZone                    // Zone (parent)
    
    // Network (parent)
    include network
  }
}
```

**Detail view: Server zone internals:**
```likec4
views 'Deployment' {
  /**
   * Server Zone Details
   * Elements: appServer (webService, apiService, cache), dbServer (database, backup)
   */
  deployment view serverZoneDetails {
    title 'Server Zone - Services & Storage'
    description 'Detailed view of server zone: app and database services'
    
    // App server services (explicit)
    include network.serverZone.appServer.webService
    include network.serverZone.appServer.apiService
    include network.serverZone.appServer.cache
    include network.serverZone.appServer          // VM (parent)
    
    // DB server services (explicit)
    include network.serverZone.dbServer.database
    include network.serverZone.dbServer.backup
    include network.serverZone.dbServer           // VM (parent)
    
    // Zone and network (parents)
    include network.serverZone
    include network
  }
}
```

## Pattern Quick Reference

| Pattern | Syntax | Use Case |
|---------|--------|----------|
| **Direct children** | `include vault.*` | Show immediate children |
| **All descendants** | `include vault.**` | Show complete hierarchy |
| **Incoming relationships** | `include -> vault.*` | What calls this? |
| **Outgoing relationships** | `include vault.* ->` | What does this call? |
| **Tag filtering** | `include ** where tag is #Vm` | Show only VMs |
| **Multiple tags** | `include ** where tag is #Vm, ** where tag is #Prod` | Combine filters |
| **Directed tier includes** | `include tier1._ ->, -> tier2._` | Tier-to-tier flows |
| **External dependencies** | `include * where tag is #External` | All external systems |

## When to Use Each Pattern

**Use explicit includes when:**
- ✅ Creating production deployment views (maintainability)
- ✅ Documentation is critical (self-documenting architecture)
- ✅ Hierarchy should be obvious from code

**Use wildcards when:**
- ⚠️ Rapid prototyping or exploration
- ⚠️ Views should adapt dynamically to new elements
- ⚠️ Consistent tagging is maintained

**Use tag filtering when:**
- ✅ Maintaining consistent tagging (e.g., `#Vm`, `#External`)
- ✅ Views should automatically include new elements with tags
- ✅ Creating dynamic views that adapt to infrastructure changes

**Use relationship-based includes when:**
- ✅ Showing complete interaction context
- ✅ Creating focused views of how elements connect
- ✅ Highlighting dependencies (incoming and outgoing)

## File Organization Patterns

### Single-File Project
```
project/
  model.c4                        # Elements + views together
```

### Multi-File Project (Recommended)
```
project/
  system-model.c4                 # Elements, containers, components
  system-views.c4                 # views 'C1'/'C2'/'C3' + index
  system-sequences.c4             # views 'Use Cases' { }
  deployment.c4                   # Deployment nodes and VMs
  deployment-views.c4             # views 'Deployment' { }
  operations.c4                   # Operations infrastructure
  operations-views.c4             # views 'Operations' { }
```

**Benefits:**
- Separation of concerns (model vs. views)
- Easier to navigate and maintain
- Clear file-to-category mapping
- Supports larger projects
