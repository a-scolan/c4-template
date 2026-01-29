# ADR-0005: Network Zone Architecture

## Status

Accepted

## Context

Dev-Forge infrastructure must implement defense-in-depth security through network segmentation. This isolates services, limits blast radius of security incidents, and enforces least-privilege network access.

**Security Requirements**:
- No direct Internet access to application tier
- Database tier isolated from external networks
- Clear firewall rules between zones
- Network traffic auditable and monitorable
- Alignment with organizational security policies

**Organizational Context**:
- On-premises datacenter with VLAN capability
- Existing firewall infrastructure (hardware firewalls, security groups)
- Network team manages VLAN provisioning
- Security team audits firewall rules quarterly

**Services to Deploy**:
- Forgejo web application (external access required)
- PostgreSQL database (internal only)
- Forgejo Actions runners (internal only, must access Forgejo and external package repos)
- Reverse proxy/load balancer (Internet-facing)

### Alternatives Considered

**Flat Network (No Segmentation)**:
- ✅ Simple configuration
- ✅ No firewall rules to manage
- ❌ **Violates security policy**
- ❌ Single compromise cascades to all services
- ❌ Cannot audit/limit traffic flows
- ❌ Compliance failure

**DMZ Only (Two-Tier)**:
- ✅ Simpler than three-tier
- ✅ Protects internal services from Internet
- ❌ Application and database in same zone (excessive privilege)
- ❌ Runners have direct database access (unnecessary)
- ❌ Does not isolate async processing

**Four+ Tier Architecture**:
- ✅ Maximum segmentation
- ✅ Separate zones for processing, data, monitoring, backup
- ❌ Overly complex for Dev-Forge scale
- ❌ Management overhead (many firewall rules)
- ❌ Difficult to troubleshoot connectivity issues

**Cloud-Style Security Groups** (without VLANs):
- ✅ Fine-grained, service-level control
- ✅ Works in cloud environments
- ❌ Requires SDN or cloud infrastructure (not available on-premises)
- ❌ Adds complexity without proven value for this use case

## Decision

We will implement a **three-tier network architecture** with distinct zones:

### Zone Definitions

#### 1. DMZ (Demilitarized Zone)
**Purpose**: Internet-facing edge services

**Services**:
- Reverse proxy / load balancer (HAProxy, Nginx, F5)
- TLS termination
- Rate limiting and WAF (if applicable)

**Network**: 
- VLAN 100: `10.0.100.0/24`
- Gateway: `10.0.100.1`

**Firewall Rules**:
- **Inbound**: HTTPS (443) from Internet
- **Outbound**: HTTPS (443, 3000) to AppTier only
- **Blocked**: Direct access to DataTier, ProcTier

**Characteristics**:
- Minimal service surface area
- No sensitive data stored
- Hardened OS configurations
- Frequent security updates

#### 2. AppTier (Application Tier)
**Purpose**: Application logic and services

**Services**:
- Forgejo web application
- Forgejo API backend
- Forgejo Actions scheduler

**Network**:
- VLAN 101: `10.1.0.0/24`
- Gateway: `10.1.0.1`

**Firewall Rules**:
- **Inbound**: HTTPS (3000) from DMZ only
- **Outbound**: 
  - PostgreSQL (5432) to DataTier
  - HTTP/HTTPS for external package repositories (for Actions)
- **Blocked**: Direct Internet inbound, direct access to runner containers

**Characteristics**:
- Stateless where possible (enables horizontal scaling)
- Secrets accessed via Hiera/Puppet (not stored in configs)
- Health checks exposed on management interface

#### 3. DataTier (Data/Persistence Tier)
**Purpose**: Data storage and persistent state

**Services**:
- PostgreSQL database
- File storage (Git repositories, LFS)
- (Future: backup storage)

**Network**:
- VLAN 102: `10.2.0.0/24`
- Gateway: `10.2.0.1`

**Firewall Rules**:
- **Inbound**: PostgreSQL (5432) from AppTier only
- **Outbound**: None (isolated except for backups)
- **Blocked**: All other traffic

**Characteristics**:
- No outbound Internet access
- Encrypted at rest (LUKS or equivalent)
- Daily backups to separate network/storage

### Traffic Flow Diagram

```
Internet
    ↓ HTTPS (443)
┌─────────────┐
│DMZ          │ VLAN 100
│Load Balancer│
└─────────────┘
    ↓ HTTPS (3000)
┌─────────────┐
│AppTier      │ VLAN 101
│Forgejo + Runners
└─────────────┘
    ↓ PostgreSQL (5432)
┌─────────────┐
│DataTier     │ VLAN 102
│PostgreSQL   │
└─────────────┘
  (no outbound)
```

### Runners Placement

**Forgejo Actions runners** are in AppTier:
- Need access to Forgejo API (same VLAN)
- Need outbound Internet for dependency downloads (npm, PyPI, Maven)
- Do NOT need direct database access
- Ephemeral containers (limited blast radius)

## Consequences

### Positive Consequences

- **Defense in Depth**: Multiple security boundaries—compromise in one zone does not cascade
- **Least Privilege**: Each zone only accesses what it needs (database never touches Internet)
- **Auditability**: Traffic flows are explicit and loggable at zone boundaries
- **Compliance**: Meets organizational security standards for network segmentation
- **Incident Containment**: Compromised runner cannot directly access database
- **Clear Responsibilities**: Network team manages zones, app team manages services

### Negative Consequences

- **Complexity**: Three VLANs to manage, firewall rules to maintain
- **Troubleshooting**: Network issues harder to diagnose across zone boundaries
- **Firewall Dependency**: Misconfigured rule can break connectivity
- **Change Process**: Firewall changes require network team coordination
- **Testing Overhead**: Must test connectivity between all zones during deployment

### Neutral Consequences

- **Monitoring Placement**: Monitoring agents need firewall rules to reach metrics endpoints
- **Backup Strategy**: Backups must traverse zone boundaries (requires firewall rule)
- **Future Scaling**: Additional services must be classified into zones

## Notes

### Zone Assignment Guidelines

**DMZ**: Only services that MUST be Internet-accessible
**AppTier**: Application logic that needs to communicate with multiple zones
**DataTier**: Anything storing persistent, sensitive data

### Firewall Rule Management

**Rule Naming Convention**:
```
<source-zone>-to-<dest-zone>-<protocol>-<purpose>
Example: AppTier-to-DataTier-tcp-postgres
```

**Rule Documentation**:
- Every rule must have comment explaining business purpose
- Rules reviewed quarterly (security team requirement)
- Unused rules removed after 90 days

### Staging vs Production

**Identical zone architecture** but separate VLANs:

| Zone | Staging VLAN | Production VLAN |
|------|--------------|-----------------|
| DMZ | 100 (10.0.100.0/24) | 200 (10.0.200.0/24) |
| AppTier | 101 (10.1.0.0/24) | 201 (10.1.0.0/24) |
| DataTier | 102 (10.2.0.0/24) | 202 (10.2.0.0/24) |

### Future Zones (Deferred)

**ProcTier (Processing Tier)**:
- If async processing needs stronger isolation from app tier
- Would sit between AppTier and DataTier
- For message queues, background workers, batch processing

**SecZone (Security/Monitoring)**:
- Dedicated zone for monitoring, logging, security scanning
- Sideband network for health checks
- Deferred until monitoring requirements mature

### Emergency Access

**Break-glass Procedure**:
- SSH bastion host in DMZ (restricted IP source, MFA required)
- Temporary firewall rules with automatic expiration (4 hours)
- All emergency access logged and audited

### Related Decisions

- [ADR-0003: Puppet Automation](0003-puppet-automation.md) — Puppet enforces zone configuration
- [ADR-0002: Actions Scalability](0002-actions-scalability.md) — Runners placed in AppTier

### References

- Network Segmentation Best Practices: NIST SP 800-82
- Organizational Network Security Policy (Confluence: "Security/Network")
- Firewall Change Request Process (ServiceNow: "Firewall CR Template")
