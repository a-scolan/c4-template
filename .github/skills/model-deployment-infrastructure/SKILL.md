---
name: model-deployment-infrastructure
description: Use when modeling deployment infrastructure (environments, zones, VMs, apps, instanceOf links). Covers hierarchy, naming conventions ({Environment}{Service}Vm), rich descriptions with network specs.
---

# Model Deployment Infrastructure

## Overview

Defines how to model physical deployment infrastructure in `deployment.c4` and `operations.c4` files: Environment → Zone → VM → Node_App hierarchy, naming conventions, rich Markdown table descriptions with network specs, and `instanceOf` links to system model containers. Relationships are inherited automatically from the system model, so deployment relationships should stay rare and infrastructure-specific.

## When to Use

- Creating a new deployment environment (Production, Staging, Dev, Test)
- Adding VMs, zones, or deployment nodes to an existing environment
- Linking deployed app instances to system model containers via `instanceOf`
- Documenting infrastructure specs (IPs, OS, CPU, RAM, RTO) in VM descriptions

**Default stance:** do not add application relationships or protocol details in deployment models/views. Put those on system-model relationships and let LikeC4 propagate them through `instanceOf`.

**Do not use** for system model elements (containers, components) — use `create-element`. For zone layering and firewall rules, use `structure-deployment-tiers`.

**Keywords:** deployment, infrastructure, VM, zone, environment, instanceOf, VLAN, network, tier, hierarchy

**Next steps:** For advanced tier organization, see `structure-deployment-tiers` skill.

## Quick Reference

| Task | Recommended Pattern |
|------|----------------------|
| Name a VM | `{Environment}{Service}Vm` (e.g., `ProdUploadVm`) |
| Name a zone | `{Function}Zone` or `{Tier}Tier` |
| Build hierarchy | Environment → Zone → VM → Node_App |
| Link runtime to model | `instanceOf` with container FQN |
| Handle relationships | Inherit from system model by default |
| Document VM specs | Markdown table with `eth0` first |
| Add metadata | Only if queried by automation/compliance |

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

**Critical:** You do NOT need to create deployment relationships explicitly. They are inherited automatically from the system model, including the logical relationship label and its technology value:

```likec4
// system-model.c4
api -[calls]-> uploadService 'Route uploads' {
  technology 'HTTP/8080'
}

uploadService -[async]-> jobQueue 'Queue jobs' {
  technology 'AMQP'
}

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

**Result:** Deployment views automatically show inherited relationships between instances, with no duplication needed. If you want to show `HTTP/8080`, `HTTPS`, `AMQP`, `LDAP`, or `Manual`, put that value on the system-model relationship instead of repeating it on deployment edges.

**When to add deployment relationships:** Only for infrastructure-specific connections NOT in the system model (for example monitoring systems, backup agents, bastion access, log collectors, replication links, or an explicit network hop that matters operationally). Keep them sparse and do not duplicate normal application traffic.

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

## Common Mistakes

❌ **VMs floating outside zones** — every VM must be nested inside a zone; zones must be nested inside an environment

❌ **Missing `instanceOf` link** — every `Node_App` must reference a Container from the system model via `instanceOf FQN`

❌ **Creating deployment relationships manually** — relationships between deployed apps are inherited automatically from the system model via `instanceOf`; don’t duplicate them just to show `HTTPS`, `HTTP/8080`, database ports, or other technical details already captured in the logical model

❌ **Omitting network interface in description** — eth0 (and eth1 if dual-homed) must be the first rows in every VM description table

❌ **Hostname repeated in metadata** — the hostname is already in the element title; don’t duplicate it in the metadata block

## Checklist

- [ ] Element kinds from shared spec (no custom kinds)
- [ ] Hierarchy: Environment → Zone → VM → Node_App
- [ ] VM naming: `{Env}{Service}Vm` (e.g., `ProdUploadVm`)
- [ ] Zone naming: `{Tier}Tier` or `{Func}Zone`
- [ ] Each VM has Markdown table with eth0, OS, CPU, RAM, Port, RTO
- [ ] Each zone has VLAN/CIDR network info
- [ ] Node_App references model Container via `instanceOf` (relationships are inherited automatically)
- [ ] Only add deployment relationships for infrastructure-specific connections (monitoring, backups, bastion access, replication, etc.)