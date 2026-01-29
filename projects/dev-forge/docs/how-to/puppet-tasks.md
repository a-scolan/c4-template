# How-To: Puppet Tasks for Dev-Forge

This guide provides expected outcomes for common Puppet-driven deployment tasks without detailing implementation (existing Puppet practices apply).

---

## Prerequisites

- Access to Puppet control repository
- Understanding of organizational Puppet conventions
- Permissions to trigger Puppet runs

---

## Deploy Forgejo Instance

### Expected Outcome

A fully configured Forgejo instance:
- Service running on designated VM
- PostgreSQL database initialized
- Configuration file (`app.ini`) deployed with organizational defaults
- HTTPS certificate configured
- Reverse proxy/load balancer integration complete

### Trigger Deployment

```bash
# Apply Puppet manifest for Forgejo
puppet agent -t --tags forgejo
```

### Verification

After Puppet run completes:
- Service accessible at `https://forge.company.internal`
- Health check endpoint returns 200: `curl -I https://forge.company.internal/api/healthz`
- Admin account created (credentials in secrets management system)

---

## Deploy Forgejo Actions Runners

### Expected Outcome

Runner pool deployed according to configuration:
- Specified number of runner VMs provisioned (3-5 for staging)
- Docker runtime installed and configured
- Runners registered with Forgejo instance
- Auto-scaling controller service active
- Network connectivity to Forgejo server verified

### Trigger Deployment

```bash
# Deploy runner infrastructure
puppet agent -t --tags forgejo-runners
```

### Verification

- Runners appear in Forgejo admin panel: **Site Administration** → **Actions** → **Runners**
- Runner status shows "idle"
- Test workflow executes successfully (see [First Pipeline Tutorial](../tutorial/02-first-pipeline.md))

---

## Scale Runner Pool

### Expected Outcome

Runner count adjusted to meet workload demands:
- Additional runner VMs provisioned (or decommissioned)
- Each runner registered with unique identifier
- Load balancer configuration updated (if applicable)
- Monitoring alerts adjusted for new capacity

### Trigger Scaling

```bash
# Scale runner pool (count defined in Puppet parameters)
puppet agent -t --tags forgejo-runners-scale
```

### Verification

- New runner count matches parameter configuration
- All runners show "idle" or "busy" status (no offline runners)
- Queue depth decreases under load (see [Configure Runners](configure-runners.md))

---

## Update Forgejo Configuration

### Expected Outcome

Configuration changes applied without service downtime:
- Updated `app.ini` deployed to Forgejo server
- Service gracefully reloaded (or restarted if required)
- Active sessions preserved (where possible)
- Audit log entry created

### Trigger Update

```bash
# Apply configuration changes
puppet agent -t --tags forgejo-config
```

### Verification

- Configuration changes visible: `sudo grep "<changed_parameter>" /etc/forgejo/app.ini`
- Service remains healthy: `systemctl status forgejo`
- Web interface accessible and functions normally

---

## Deploy PostgreSQL Database

### Expected Outcome

Dedicated PostgreSQL instance for Forgejo:
- PostgreSQL service running on designated VM
- Database and user created with appropriate permissions
- Connection pooling configured (if using PgBouncer)
- Backups scheduled and verified
- Network firewall rules allow only Forgejo server connections

### Trigger Deployment

```bash
# Deploy PostgreSQL for Forgejo
puppet agent -t --tags forgejo-database
```

### Verification

- Database accessible from Forgejo server: `psql -h db.company.internal -U forgejo -d forgejo -c "SELECT 1;"`
- Forgejo connects successfully (check logs): `sudo journalctl -u forgejo -n 50`
- Initial schema created (tables exist)

---

## Configure Network Security

### Expected Outcome

Network zones and firewall rules established:
- **DMZ zone**: Reverse proxy/load balancer accessible from Internet
- **AppTier zone**: Forgejo server isolated, accepts only from DMZ
- **DataTier zone**: PostgreSQL isolated, accepts only from AppTier
- Firewall rules enforced at zone boundaries
- Security group assignments verified

### Trigger Configuration

```bash
# Apply network security policy
puppet agent -t --tags network-security
```

### Verification

- Test external access: `curl https://forge.company.internal` (succeeds)
- Test direct database access from external: `psql -h db.company.internal` (fails/timeout)
- Review firewall logs for denied attempts
- Verify security group membership in infrastructure dashboard

---

## Provision Staging Environment

### Expected Outcome

Complete staging environment deployed:
- All VMs provisioned in staging network zone
- Forgejo, runners, and database services deployed
- Configuration uses staging-specific parameters
- Monitoring agents installed and reporting
- Environment tagged for identification (`environment=staging`)

### Trigger Provisioning

```bash
# Deploy complete staging environment
puppet agent -t --environment staging --tags devforge-full
```

### Verification

- All services healthy in monitoring dashboard
- Can complete end-to-end workflow:
  1. Create repository
  2. Push code with CI/CD workflow
  3. Verify pipeline executes
  4. Merge pull request
- Environment isolated from production (separate VLANs/subnets)

---

## Backup and Restore

### Expected Outcome (Backup)

Automated backup of critical data:
- PostgreSQL database backed up daily
- Forgejo repositories backed up to object storage
- Configuration files versioned in backup repository
- Backup verification tests successful
- Retention policy enforced (staging: 7 days)

### Expected Outcome (Restore)

System restored from backup:
- Database restored to specified point-in-time
- Repositories restored from backup
- Configuration reapplied
- Service validation confirms integrity

### Trigger Backup

```bash
# Backup is automated, but can be triggered manually
puppet agent -t --tags forgejo-backup
```

### Trigger Restore

```bash
# Restore from latest backup
puppet agent -t --tags forgejo-restore
```

### Verification (Restore)

- Restored data matches expected timestamp
- Random repository check shows complete history
- User accounts and permissions intact
- All services return to operational state

---

## Troubleshooting

### Puppet Run Fails

**Check**:
- Puppet agent service status: `systemctl status puppet`
- Puppet server connectivity: `puppet agent -t --noop`
- Last run report: `puppet agent --last-run-report`

**Resolution**: Review Puppet logs for specific error, verify network connectivity to Puppet server

### Service Not Starting After Deployment

**Check**:
- Service status: `systemctl status <service>`
- Service logs: `journalctl -u <service> -n 100`
- Configuration syntax: For Forgejo, `forgejo --check`

**Resolution**: Verify configuration syntax, check file permissions, review systemd unit file

### Configuration Not Applied

**Check**:
- Puppet run completed successfully (exit code 0)
- Target file modified: `ls -l /etc/forgejo/app.ini`
- File content: `grep "<parameter>" /etc/forgejo/app.ini`

**Resolution**: Verify Puppet facts are correct (`facter`), check module version matches expectation

---

## Expected Puppet Module Structure

*For reference* — actual implementation follows organizational conventions:

```
puppet/modules/devforge/
├── manifests/
│   ├── forgejo.pp          # Forgejo application deployment
│   ├── runners.pp          # Actions runner deployment
│   ├── database.pp         # PostgreSQL configuration
│   └── networking.pp       # Security groups and firewall
├── templates/
│   └── app.ini.erb         # Forgejo configuration template
├── files/
│   └── systemd/            # Systemd unit files
└── hiera/
    ├── staging.yaml        # Staging environment parameters
    └── production.yaml     # Production environment parameters
```

---

## Next Steps

- **Validate deployments**: Use monitoring to verify service health
- **Automate further**: Integrate Puppet runs into CI/CD pipelines
- **Document customizations**: Maintain organizational Puppet conventions documentation

## Related Documentation

- [How-To: Configure Runners](configure-runners.md) — Runner-specific configuration
- [How-To: Setup Plugins](setup-plugins.md) — Plugin activation post-deployment
- [Explanation: Puppet Automation (ADR-0003)](../../ADR/0003-puppet-automation.md) — Automation strategy rationale
