---
name: model-deployment-infrastructure
description: Use when modeling deployment infrastructure (environments, zones, VMs, apps, instanceOf links). Covers hierarchy, naming conventions ({Environment}{Service}Vm), rich descriptions with network specs.
---

# Model Deployment Infrastructure

Use this skill when defining physical infrastructure in deployment.c4 and operations.c4 files.

**Keywords:** deployment, infrastructure, VM, zone, environment, instanceOf, VLAN, network, tier, hierarchy

**Next steps:** For advanced tier organization, see `structure-deployment-tiers` skill.

## Core Requirements

| Requirement | Rule |
|-------------|------|
| **Element kinds** | Use shared spec kinds from `spec-deployment.c4` (don't create custom ones) |
| **Element tags** | Use shared spec tags (#Production, #Networking, #Service, #Monitoring) |
| **Naming formula** | VMs: `{Environment}{ServiceName}Vm`; Zones: `{Tier}Tier` or `{Function}Zone` |
| **Hierarchy** | Always: Environment → Zone → VM → Node_App |
| **Rich descriptions** | Use Markdown tables with specs (eth0, OS, CPU, RAM, Port, RTO) |
| **Metadata** | Optional - only add if automation queries these fields |
| **instanceOf** | Link Node_App to model Container using FQN - relationships are inherited automatically |

## Naming Convention Patterns

### Virtual Machines (VMs)

**Pattern:** `{Environment}{ServiceName}Vm` (PascalCase)

```likec4
ProdApigwVm      // prod + apigw (API gateway) + Vm
ProdUploadVm     // prod + upload + Vm
StagingApiVm     // staging + api + Vm
DevDatabaseVm    // dev + database + Vm
```

**Rules:**
- Environment: `Prod`, `Staging`, `Dev`, `Test`
- Service name: Meaningful abbreviation
- Suffix: Always `Vm` (consistent casing)

### Zones (Network Segments)

**Pattern:** `{Tier}Tier` for layered architecture or `{Function}Zone` for specialized infrastructure

```likec4
// Tier-based (standard)
Dmz         // Demilitarized Zone (edge security)
AppTier     // Application tier (microservices)
ProcTier    // Processing tier (async workers)
DataTier    // Data tier (databases, storage)

// Function-based (optional)
SecZone     // Security & monitoring
InfraZone   // Backup & disaster recovery
```

### Environments

**Pattern:** Single word, PascalCase

```likec4
Prod        // Production
Staging     // Staging/pre-production
Dev         // Development
Test        // Testing
```

## Hierarchy Structure

**ALWAYS maintain parent-child relationships:**

```
Node_Environment (Production/Staging/Dev)
  └─ Zone (Tier or Function)
      └─ Node_Vm (Infrastructure)
          └─ Node_App (instanceOf Container from system-model)
```

**Critical:** VMs never float outside zones, zones never float outside environments.

## Rich Descriptions: Markdown Tables

Every VM and zone should include a Markdown table with specs. **Always put network interfaces first (eth0, eth1):**

```likec4
ProdUploadVm = Node_Vm "prod-upload-vm" {
  #Production
  technology "Node.js + Docker"
  
  description """
    File upload and validation service (fail-fast pattern)
    
    | Property | Value |
    |:---------|:------|
    | eth0 | 10.1.0.12/24 |
    | OS | Ubuntu 22.04 LTS |
    | CPU | 2 vCPU |
    | RAM | 4 GB |
    | Disk | 100 GB SSD |
    | Port | 3001 |
    | Container | Docker |
    | Monitoring | Prometheus 9090 |
    | RTO | 5 minutes |
  """
  
  uploadApp = Node_App "Upload Service" {
    instanceOf vault.uploadService
  }
}
```

**Zone description template:**

```likec4
AppTier = Zone "Application Tier (VLAN 101: 10.1.0.0/24)" {
  description """
    Microservices production environment
    
    | Property | Value |
    |:---------|:------|
    | VLAN | 101 |
    | Network | 10.1.0.0/24 |
    | Gateway | 10.1.0.1 |
    | Firewall | Ingress from DMZ on 443 |
    | Firewall | Egress to DataTier on 27017 |
    | Purpose | Production microservices |
  """
}
```

## Relationship Inheritance via instanceOf

**Critical:** You do NOT need to create deployment relationships explicitly. They are inherited automatically from the system model:

```likec4
// system-model.c4
api -[calls]-> uploadService 'Route uploads'
uploadService -[async]-> jobQueue 'Queue jobs'

// deployment.c4 (relationships inherited automatically via instanceOf)
Prod.Dmz.ProdApigwVm.apiApp {  // When you do:
  instanceOf vault.api          // This Node_App inherits all relationships from vault.api
}

Prod.AppTier.ProdUploadVm.uploadApp {
  instanceOf vault.uploadService  // Automatically inherits: api -> uploadService
}

Prod.ProcTier.ProdQueueVm.queueApp {
  instanceOf vault.jobQueue       // Automatically inherits: uploadService -> jobQueue
}
```

**Result:** Deployment views automatically show inherited relationships between instances, with no duplication needed.

**When to add deployment relationships:** Only for infrastructure-specific connections NOT in the system model (e.g., monitoring systems, backup agents, log collectors).

## Optional: Metadata Fields

Only add metadata if automation queries these fields:

```likec4
// ✅ Minimal (recommended)
metadata {
  eth0 '10.1.0.12/24'    // Only if network automation needs this
  rto '5 min'            // Only if SLA automation needs this
}

// ❌ Avoid (over-detailed)
metadata {
  eth0 '10.1.0.12/24'
  hostname 'prod-upload-vm'  // Redundant - already in title
  cpu '2 vCPU'               // Already in markdown table
  ram '4 GB'                 // Already in markdown table
  kernel '5.15'              // Unnecessary for deployment context
}
```

## Multiple instanceOf (Shared Services)

If a single deployed unit serves multiple logical containers:

```likec4
ldapInstance = Node_App "LDAP Service" {
  instanceOf chaineInterne.annuaire.ldapInterne
  instanceOf chaineExterne.annuaire.ldapExterne
}
```

**Guideline:** Use multiple `instanceOf` only when services are truly deployed together and managed as one unit. Otherwise, create separate Node_App instances.

## Complete Examples

For comprehensive multi-environment setups with all tiers, zone descriptions, VM specifications, and inter-tier relationships, reference the examples in your project's deployment.c4 file or multi-tier patterns in `structure-deployment-tiers`skill.

## Related Skills

- **structure-deployment-tiers** — Advanced: organizing zones into DMZ→AppTier→ProcTier→DataTier with firewall rules
- **write-rich-descriptions** — Markdown table formatting for deployment specs
- **design-view** — Creating deployment views that visualize this infrastructure

## Checklist

- [ ] Element kinds from shared spec (no custom kinds)
- [ ] Hierarchy: Environment → Zone → VM → Node_App
- [ ] VM naming: `{Env}{Service}Vm` (e.g., `ProdUploadVm`)
- [ ] Zone naming: `{Tier}Tier` or `{Func}Zone`
- [ ] Each VM has Markdown table with eth0, OS, CPU, RAM, Port, RTO
- [ ] Each zone has VLAN/CIDR network info
- [ ] Node_App references model Container via `instanceOf` (relationships are inherited automatically)
- [ ] Only add deployment relationships for infrastructure-specific connections (monitoring, backups, etc.)