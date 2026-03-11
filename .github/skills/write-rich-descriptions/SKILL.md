---
name: write-rich-descriptions
description: Use when adding structured descriptions to LikeC4 elements — metadata blocks for system models (queryable by automation), markdown tables for deployment infrastructure (VM specs, network interfaces, RTO). Decides format based on element type and whether fields will be queried.
---

# Write Rich Descriptions

## Overview

Selects the right description format for each element type: `metadata { }` blocks for system-level elements (structured and queryable by automation), markdown tables for deployment nodes (human-readable infrastructure specs). Only adds fields that are actually queried or useful to operators.

## When to Use

- When creating or documenting system-level elements (containers, services, components)
- When documenting deployment nodes (VMs, zones) with network and hardware specs
- When model needs to be queryable by owner, region, or infrastructure properties
- When onboarding operators who need to understand network topology at a glance

## Quick Reference

| Context | Format | Why | File |
|---------|--------|-----|------|
| **System Models** | `metadata { }` blocks | Queryable, filterable, structured | `system-model.c4` |
| **Deployment Models** | Markdown tables | Human-readable specs | `deployment.c4` |

**Prerequisite:** Element has been created. See `create-element` or `model-deployment` for basic structure.

## Core Principle: Metadata is Optional, Sparse by Default

**Only add metadata if you actually query/filter by those fields.** Default: just technology + description.

---

## Four Step Workflow

### 1. Choose Format Based on Element Type

**Markdown tables (tables, not metadata) for:**
- VMs and bare metal servers (show eth0, OS, CPU, RAM, Disk, RTO)
- Zones and network segments (show VLAN, Network, Gateway)
- Infrastructure elements

**Metadata blocks (optional, only if querying) for:**
- System-level: owner or team (for auto-assignment)
- System-level: regions (if multi-region matters)
- Deployment: network IPs, OS, CPU, RAM, RTO/RPO (if using for automation)

**NO metadata needed for:**
- Components
- Most containers (unless you filter by owner)
- Compliance/test data (belongs in CI pipeline, not model)

### 2. Structure the Description

**System models (minimal example):**
```likec4
uploadService = Container_Service 'Upload Service' {
  #backend #microservice
  technology 'Node.js / Express 4.18'
  
  description """
    Handles file uploads and validates content.
    
    **Responsibilities:**
    - Receive multipart file uploads
    - Fail-fast validation (size, type)
    - Queue validated files
  """
}
```

**If you need ownership (optional):**
```likec4
uploadService = Container_Service 'Upload Service' {
  #backend #microservice
  technology 'Node.js / Express 4.18'
  description "Handles file uploads and validates content."
  
  metadata {
    owner 'alice@company.com'  // Only if auto-assigning tickets
  }
}
```

**NOTE: SLA/RTO/RPO belong at SYSTEM level, not individual containers.**

**Deployment models (mandatory table, optional metadata):**
```likec4
ProdUploadVm = Node_Vm "prod-upload-vm" {
  technology 'Node.js + Docker'
  
  description """
    File upload handler and validation service.
    
    | Property | Value |
    |:---------|:------|
    | eth0 | 10.1.0.12/24 |
    | OS | Ubuntu 22.04 LTS |
    | CPU | 2 vCPU |
    | RAM | 4 GB |
    | Disk | 100 GB SSD |
    | RTO | 5 min |
  """
  
  metadata {
    eth0 '10.1.0.12/24'  // Only if automation queries this
    os 'Ubuntu 22.04'
    cpu '2 vCPU'
    ram '4 GB'
    disk '100 GB SSD'
    rto '5 min'
  }
}
```

**Metadata in deployment is optional:** Include it only if you're querying for inventory/compliance/capacity planning.

### 3. Follow Format-Specific Rules

#### Metadata Block Rules (System Models)

**ONLY add if you filter/query by the field:**

```likec4
// ✅ Good - querying by owner for auto-assignment
apiService = Container_Service 'API' {
  technology 'Go'
  description 'REST API'
  
  metadata {
    owner 'alice@company.com'
  }
}

// ✅ Good - querying regions for multi-region setup
apiService = Container_Service 'API' {
  technology 'Go'
  description 'REST API'
  
  metadata {
    regions ['us-east-1', 'eu-west-1']  // Only if you filter by region
  }
}

// ❌ Bad - never use SLA at container level (use at SYSTEM level instead)
apiService = Container_Service 'API' {
  metadata {
    sla '99.9%'  // WRONG - belongs on System, not container
  }
}

// ❌ Bad - don't duplicate tags
apiService = Container_Service 'API' {
  #backend #critical
  metadata {
    tags ['backend', 'critical']  // Already defined via #tags!
  }
}
```

**Multiple values (use arrays if needed):**
```likec4
metadata {
  regions ['us-east-1', 'eu-west-1']
  contact_channels ['team@company.com', '#team-slack']
}
```

**If you never query it, don't add it.**

#### Markdown Table Rules (Deployment Models)

**Network interfaces ALWAYS first:**
```likec4
description """
  | Property | Value |
  |:---------|:------|
  | eth0 | 10.1.0.12/24 |     ← FIRST (operators need network info immediately)
  | eth1 | 10.4.0.12/24 |
  | OS | Ubuntu 22.04 |
  | CPU | 2 vCPU |
  | RAM | 4 GB |
"""
```

**Standard property order (when applicable):**
1. Network interfaces (eth0, eth1, ...) — FIRST
2. Operating System
3. Hardware (CPU, RAM, Disk)
4. Application/Service details
5. Operational (RTO, RPO, Health Check)

**Only include relevant properties** — these templates are reference examples, not checklists.

### 4. Metadata for Automation (Optional Deployment)

**If you have automation that queries the model, duplicate key fields into metadata:**

```likec4
ProdDbVm = Node_Vm "prod-db-vm" {
  description """
    Primary database server.
    
    | eth0 | 10.2.0.10/24 |
    | OS | Ubuntu 22.04 |
    | RTO | 2 min |
  """
  
  metadata {
    eth0 '10.2.0.10/24'  // Automation queries this
    os 'Ubuntu 22.04'
    rto '2 min'
  }
}
```

**If no automation queries the model, skip the metadata block entirely.**

## System Model: Minimal by Default

### Container/Service - Baseline

```likec4
uploadService = Container_Service 'Upload Service' {
  #backend #microservice
  technology 'Node.js / Express 4.18'
  
  description """
    Handles file uploads and validates content.
    
    **Responsibilities:**
    - Receive uploads
    - Validate (size, type)
    - Queue for processing
  """
}
```

**Add metadata only if truly needed:**
```likec4
uploadService = Container_Service 'Upload Service' {
  technology 'Node.js / Express'
  description 'Handles file uploads...'
  
  metadata {
    owner 'alice@company.com'  // If auto-assigning ownership
  }
}
```

**DO NOT put here:** team, sla, rto, rpo, framework_version, compliance_tags, contact_channels, dependencies
- SLA/RTO/RPO: System level only
- Team/owner: Just use owner if needed; drop team entirely
- Framework version: Already in technology field
- Everything else: Belongs in docs/CI pipeline, not model

### Component - No Metadata

```likec4
validateModule = Component 'File Validator' {
  #validation #security
  technology 'TypeScript'
  
  description 'Validates uploads: size, type, malware scan.'
}
```

**Components never need metadata.**

## Deployment Model: Tables First, Metadata Optional

### Zone Template

```likec4
AppTier = Zone "Application Tier (VLAN 101: 10.1.0.0/24)" {
  description """
    Production microservices deployment zone.
    
    | Property | Value |
    |:---------|:------|
    | VLAN | 101 |
    | Network | 10.1.0.0/24 |
    | Gateway | 10.1.0.1 |
    | Monitoring Port | 9090 |
  """
  
  metadata {
    vlan '101'
    network '10.1.0.0/24'
    gateway '10.1.0.1'
    monitoring_port '9090'
  }
}
```

**Gateway belongs in zones** (defines subnet routing), not individual VMs (implicit to zone).

### VM Template

```likec4
ProdUploadVm = Node_Vm "prod-upload-vm" {
  technology "Node.js + Docker"
  
  description """
    File upload handler with fail-fast validation.
    
    | Property | Value |
    |:---------|:------|
    | eth0 | 10.1.0.12/24 |
    | eth1 | 10.4.0.12/24 (monitoring) |
    | OS | Ubuntu 22.04 LTS |
    | CPU | 2 vCPU |
    | RAM | 4 GB |
    | Disk | 100 GB SSD |
    | Container Runtime | Docker 20.10 |
    | Health Check | GET /health:3001 (30s) |
    | RTO | 5 min |
  """
  
  metadata {
    eth0 '10.1.0.12/24'
    eth1 '10.4.0.12/24'
    os 'Ubuntu 22.04 LTS'
    cpu '2 vCPU'
    ram '4 GB'
    disk '100 GB SSD'
    container_runtime 'Docker 20.10'
    health_check 'GET /health:3001 (30s)'
    rto '5 min'
  }
  
  uploadApp = Node_App "Upload Service" {
    instanceOf vault.uploadService
  }
}
```

**Network interfaces first** because operators need networking info immediately.

## Metadata Querying (System Models)

Metadata enables programmatic queries:

```typescript
// Find all critical services
const critical = model.elements()
  .filter(e => e.tags.includes('critical'))

// Group by team
const byTeam = new Map()
for (const element of model.elements()) {
  const team = element.getMetadata('team')
  if (team) {
    if (!byTeam.has(team)) byTeam.set(team, [])
    byTeam.get(team).push(element)
  }
}

// Find multi-region services
const multiRegion = model.elements()
  .filter(e => {
    const regions = e.getMetadata('regions')
    return Array.isArray(regions) && regions.length > 1
  })
```

## What NOT to Include (Deployment Models)

**Already defined elsewhere — don't duplicate:**

| ❌ Don't Include | ✅ Where It's Defined | Why |
|---|---|---|
| Hostname | Element title (`Node_Vm "hostname"`) | Redundant with model |
| Gateway (in VM) | Zone table (defines subnet route) | VMs inherit zone's gateway |
| Firewall rules | Diagram arrows between zones | Topology shows flows |
| Monitoring links | Diagram relationships | Relationships define monitoring |
| Service endpoints | Relationships + instanceOf | Avoid duplicating relationship data |
| Tags | Element `#tag` syntax | Tags are model properties |

**Exception:** Gateway in VM metadata for edge cases (multi-homed, policy routing).

## Best Practices

### System Models (Metadata Blocks)

1. ✅ **Use metadata { }** for structured, queryable data
2. ✅ **Prose descriptions** for narrative context
3. ✅ **Single values** for scalars (team, owner, framework)
4. ✅ **Arrays for lists** (regions, dependencies, contacts) — always explicit
5. ✅ **Group related values** (contact_channels, compliance_tags)
6. ✅ **YAML/JSON strings** for complex config (triple quotes)
7. ❌ **Don't duplicate tags** already on element
8. ✅ **Use `link`** for external resources (docs, repos, dashboards)

### Deployment Models (Markdown Tables)

1. ✅ **Single table** per element (VM, zone)
2. ✅ **Network interfaces first** (eth0, eth1, VLAN)
3. ✅ **Standard order:** Network → OS → Hardware → Service → Operational
4. ✅ **Only relevant properties** (not a checklist)
5. ✅ **Add metadata duplicate** for automation
6. ❌ **Don't include hostname** (already in element title)
7. ❌ **Don't include gateway in VMs** (zones define it)
8. ❌ **Don't duplicate relationships** (firewall, monitoring shown in diagram)

## Common Mistakes

| ❌ Mistake | ✅ Correct | Why |
|---|---|---|
| System model with tables | Metadata blocks | Queryable/filterable |
| Deployment without table | Markdown table + metadata | Dual approach for humans + automation |
| eth0 not first in table | eth0 always first | Operators need network info immediately |
| Metadata as strings not arrays | `regions: ['us-east-1', 'eu-west-1']` | Enables filtering logic |
| Tags in metadata | Use `#tag` on element | Tags are model properties |
| Hostname in VM table | Omit (in element title) | Redundant |
| Gateway in VM table | Gateway in zone table | VMs inherit zone's gateway |
| Multiple separate tables | Single table per element | Unified format easier to scan |

## Templates Reference

See [EXAMPLES.md](EXAMPLES.md) for:
- Complete system model templates (services, components, APIs)
- Complete deployment templates (zones, VMs, environments)
- Advanced metadata patterns (YAML/JSON, arrays, grouping)
- Zone vs. VM comparison
- Multi-homed network examples
- Dynamic view descriptions
- Complex infrastructure scenarios
