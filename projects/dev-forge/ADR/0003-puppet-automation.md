# ADR-0003: Puppet for Infrastructure Automation

## Status

Accepted

## Context

Dev-Forge requires automated, repeatable infrastructure provisioning and configuration management across staging and production environments. Key requirements:

**Automation Needs**:
- Deploy Forgejo application servers
- Provision Forgejo Actions runner pools
- Configure PostgreSQL databases
- Manage network security groups and firewall rules
- Maintain configuration consistency across environments
- Enable rapid environment replication (staging → production)

**Organizational Context**:
- **Puppet is already in use** across the organization
- Existing team expertise in Puppet manifests and modules
- Established Puppet infrastructure (master, agents, r10k)
- Organizational Puppet patterns and conventions documented
- Integration with existing secret management (Hiera eyaml)

**Constraints**:
- Must integrate with existing infrastructure automation
- Cannot introduce tools requiring extensive retraining
- On-premises deployment model (no cloud provisioning APIs)
- Must support environment parity (staging/production identical configs)

### Alternatives Considered

**Ansible**:
- ✅ Agentless (SSH-based)
- ✅ Simpler learning curve for beginners
- ✅ Strong community and modules
- ❌ **No existing organizational expertise**
- ❌ Would require new infrastructure setup
- ❌ Different paradigm from current practices

**Terraform**:
- ✅ Declarative infrastructure-as-code
- ✅ Excellent for cloud provisioning
- ✅ State management for infrastructure
- ❌ **Not designed for configuration management**
- ❌ Weaker at application deployment vs infrastructure provisioning
- ❌ No existing organizational expertise

**Manual Configuration**:
- ✅ No tool learning required
- ✅ Complete control
- ❌ Error-prone and non-repeatable
- ❌ Difficult to replicate staging → production
- ❌ No configuration version control
- ❌ Cannot scale beyond initial deployment

**SaltStack**:
- ✅ Fast execution (ZeroMQ transport)
- ✅ Good scalability
- ❌ **No existing organizational expertise**
- ❌ Smaller community than Puppet/Ansible
- ❌ Would fragment automation tooling

**Chef**:
- ✅ Mature configuration management
- ✅ Ruby DSL (familiar to some developers)
- ❌ **No existing organizational expertise**
- ❌ Declining popularity/community activity
- ❌ Complex ecosystem (Chef Server, workstations)

## Decision

We will use **Puppet** for all Dev-Forge infrastructure automation and configuration management.

### Rationale

1. **Existing Expertise**: Team already proficient in Puppet—no learning curve

2. **Infrastructure Integration**: Leverages existing Puppet master, r10k workflows, Hiera secrets

3. **Proven Patterns**: Can follow established organizational conventions for modules and manifests

4. **Environment Parity**: Hiera enables identical configuration with environment-specific overrides

5. **Version Control**: Puppet code naturally lives in Git (aligns with Dev-Forge itself being Git-centric)

6. **Declarative Model**: Puppet's resource abstraction ensures desired state convergence

7. **Orchestration**: Puppet orchestrator can coordinate multi-node deployments (database → app → runners)

### Scope

Puppet will manage:
- **Application deployment**: Forgejo service installation and configuration
- **Database provisioning**: PostgreSQL installation, user creation, schema initialization
- **Runner infrastructure**: VM provisioning, Docker setup, runner registration
- **Network configuration**: Firewall rules, security groups, zone assignments
- **Monitoring agents**: Prometheus node exporters, log shippers
- **Secret distribution**: Database passwords, API tokens, TLS certificates

Puppet will **not** manage:
- Forgejo application code/upgrades (handled via Forgejo's built-in update mechanism)
- Data backup strategies (separate backup tooling)
- Log aggregation backend (existing ELK stack)

## Consequences

### Positive Consequences

- **Zero Learning Curve**: Team can immediately write manifests using existing skills
- **Reuse Existing Modules**: Leverage organizational Puppet module library (PostgreSQL, firewall, etc.)
- **Infrastructure Consistency**: Same tool that manages other organizational infrastructure
- **Secret Management**: Integrated with existing Hiera eyaml encryption workflow
- **Predictable Operations**: Deployment patterns match organizational norms
- **Debugging Familiarity**: Team knows how to troubleshoot Puppet runs
- **Documentation Exists**: Internal Puppet best practices already documented

### Negative Consequences

- **Agent Overhead**: Requires Puppet agent on every managed node
- **Puppet Master Dependency**: Single point of failure (mitigated by existing HA setup)
- **Ruby Dependency**: Puppet requires Ruby runtime on nodes
- **Learning Curve for New Hires**: Puppet less common than Ansible in industry
- **Verbose Syntax**: Puppet manifests can be more verbose than Ansible playbooks

### Neutral Consequences

- **Convergence Model**: Puppet's eventual consistency model (vs imperative Ansible)
- **Catalogue Compilation**: Requires Puppet master to compile node catalogues
- **Module Ecosystem**: Puppet Forge has good coverage but smaller than Ansible Galaxy

## Notes

### Puppet Module Structure

Dev-Forge Puppet code will follow organizational structure:

```
puppet/modules/devforge/
├── manifests/
│   ├── init.pp              # Main class
│   ├── forgejo.pp           # Forgejo application
│   ├── runners.pp           # Actions runners
│   ├── database.pp          # PostgreSQL
│   └── networking.pp        # Firewall/security
├── templates/
│   └── app.ini.erb          # Forgejo configuration template
├── files/
│   └── systemd/             # Systemd unit files
└── hiera/
    ├── staging.yaml         # Staging parameters
    └── production.yaml      # Production parameters
```

### Environment Management

Hiera hierarchy enables environment differences:

```yaml
# hiera/staging.yaml
devforge::base_runner_count: 3
devforge::database_host: 'db-staging.company.internal'
devforge::domain: 'forge-staging.company.internal'

# hiera/production.yaml
devforge::base_runner_count: 8
devforge::database_host: 'db-prod.company.internal'
devforge::domain: 'forge.company.internal'
```

### Integration Points

- **r10k**: Dev-Forge Puppet code deployed via existing r10k workflow
- **PuppetDB**: Query infrastructure state for monitoring/reporting
- **Foreman**: (if used) VM provisioning triggers Puppet classification
- **Hiera**: Secrets managed via existing eyaml infrastructure

### Alternative for Specific Tasks

While Puppet is the primary tool, certain tasks may use specialized tools:
- **TLS certificate renewal**: Existing cert-manager or ACME client
- **Backup orchestration**: Existing backup solution (Bacula, Bareos, etc.)
- **Monitoring**: Existing Prometheus/Grafana infrastructure

### Related Decisions

- [ADR-0002: Actions Scalability](0002-actions-scalability.md) — Puppet orchestrates runner auto-scaling
- [ADR-0005: Network Zones](0005-network-zones.md) — Puppet enforces network segmentation

### References

- Organizational Puppet Style Guide (Confluence: "Infrastructure/Puppet")
- Puppet Best Practices: https://puppet.com/docs/puppet/latest/style_guide.html
- Existing Puppet Modules: Internal GitLab/Forgejo repository
