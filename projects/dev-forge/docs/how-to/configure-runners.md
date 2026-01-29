# How-To: Configure Runners for Forgejo Actions

This guide shows you how to configure and scale Forgejo Actions runners for your CI/CD workloads.

---

## Prerequisites

- Administrator access to Dev-Forge infrastructure
- Understanding of Forgejo Actions (see [First Pipeline Tutorial](../tutorial/02-first-pipeline.md))
- Access to Puppet configuration repository

---

## Understanding Runner Architecture

Dev-Forge uses **containerized runners** that execute CI/CD workflows in isolated environments. The runner pool consists of:

- **3-5 base runners** (initial staging configuration)
- **Auto-scaling** based on queue depth
- **Docker-based** execution for isolation
- **Technology-agnostic** supporting any language/framework

---

## Check Current Runner Status

### From Forgejo Web Interface

1. Navigate to **Site Administration** → **Actions** → **Runners**
2. View active runners with:
   - Runner name and ID
   - Status (idle, busy, offline)
   - Last seen timestamp
   - Completed jobs count

### Expected Output

For a healthy staging environment, you should see 3-5 runners with "idle" or "busy" status and recent "last seen" times (within 60 seconds).

---

## Configure Runner Count

### Adjust Base Runner Pool

The base runner count determines how many runners are always available:

**Expected configuration location**: Puppet manifest (`runners.pp`)

**Expected parameters**:
```puppet
# Base runner count (always running)
$base_runner_count = 3

# Maximum runners (auto-scale limit)
$max_runner_count = 10
```

**To modify**:
1. Update the `$base_runner_count` parameter
2. Apply Puppet configuration (see [Puppet Tasks Guide](puppet-tasks.md))
3. Verify new runners appear in Forgejo admin panel

**When to increase base count**:
- Consistent queue depth > 0 during normal hours
- Workflows frequently wait for available runners
- Team size grows beyond 10 active developers

---

## Configure Auto-Scaling

### Queue-Based Scaling

Auto-scaling triggers when the workflow queue exceeds thresholds:

**Expected configuration**:
```puppet
# Scale up when queue depth exceeds threshold
$scale_up_threshold = 2

# Scale down delay (minutes of idle time)
$scale_down_delay = 15

# Check interval (seconds)
$scaling_check_interval = 30
```

**To adjust thresholds**:

**If workflows wait too long** → Decrease `$scale_up_threshold` to 1  
**If runners spin up/down frequently** → Increase `$scale_down_delay` to 30  
**If scaling reacts slowly** → Decrease `$scaling_check_interval` to 15

### Verify Scalabilty

Trigger multiple workflows simultaneously to test auto-scaling:

```bash
# Clone test repository
git clone https://forge.yourcompany.internal/admin/scaling-test.git
cd scaling-test

# Trigger 10 concurrent workflows
for i in {1..10}; do
  echo "Test run $i" >> test.txt
  git add test.txt
  git commit -m "Trigger workflow $i"
  git push origin main &
done
wait
```

Monitor the **Runners** page to observe:
- Queue depth increasing
- New runners appearing (within 1-2 minutes)
- Workflows distributing across runners
- Runners scaling down after 15 minutes idle

---

## Configure Runner Resources

### CPU and Memory Allocation

Each runner container requires resources based on typical workflows:

**Expected defaults** (per runner):
- **CPU**: 2 vCPU
- **Memory**: 4 GB RAM
- **Disk**: 20 GB ephemeral storage

**To modify resource limits**:

Update Puppet configuration:
```puppet
$runner_cpu_limit = '2.0'
$runner_memory_limit = '4G'
$runner_disk_limit = '20G'
```

**When to increase resources**:
- Build-heavy workflows (compilation, packaging)
- Memory-intensive tests (integration, E2E)
- Large monorepo checkouts

**Example profiles**:

| Workflow Type | CPU | Memory | Disk |
|---------------|-----|--------|------|
| Linting/Tests | 1.0 | 2 GB | 10 GB |
| Standard Build | 2.0 | 4 GB | 20 GB |
| Heavy Build | 4.0 | 8 GB | 50 GB |

---

## Configure Runner Labels

Labels allow targeting specific runners for specialized workflows.

**Expected labeling scheme**:
- `ubuntu-latest`: Default Linux runners
- `docker`: Runners with Docker-in-Docker capability
- `high-memory`: Runners with 8+ GB RAM
- `gpu`: Runners with GPU access (future)

**To add labels**:

Configure in Puppet:
```puppet
forgejo_runner { 'runner-1':
  labels => ['ubuntu-latest', 'docker'],
}

forgejo_runner { 'runner-heavy':
  labels => ['ubuntu-latest', 'docker', 'high-memory'],
  memory => '8G',
  cpu    => '4.0',
}
```

**Use labels in workflows**:
```yaml
jobs:
  build:
    runs-on: high-memory
    steps:
      - name: Heavy build task
        run: make build-large-app
```

---

## Monitor Runner Health

### Key Metrics to Track

1. **Queue depth**: Should remain 0-1 during normal operations
2. **Runner utilisation**: 40-70% is healthy (room for spikes)
3. **Workflow failure rate**: < 5% (excluding code issues)
4. **Average queue wait time**: < 30 seconds

### Check Metrics

**From Forgejo admin panel**:
- Site Administration → Actions → Statistics

**From Prometheus** (if monitoring configured):
```
forgejo_actions_queue_depth
forgejo_actions_runner_idle_count
forgejo_actions_runner_busy_count
forgejo_actions_workflow_duration_seconds
```

---

## Troubleshooting

### Runners Show Offline

**Check**:
1. Runner service status on VM: `systemctl status forgejo-runner`
2. Network connectivity from runner VM to Forgejo server
3. Runner registration token validity

**Resolution**: See [Puppet Tasks Guide](puppet-tasks.md) for re-registering runners

### Workflows Queue Indefinitely

**Check**:
1. All runners are at capacity (busy)
2. Workflow specifies unavailable label
3. Auto-scaling disabled or misconfigured

**Resolution**: Increase `$base_runner_count` or verify auto-scaling parameters

### Auto-Scaling Not Working

**Check**:
1. Scaling controller service: `systemctl status forgejo-runner-scaler`
2. Controller logs: `journalctl -u forgejo-runner-scaler -f`
3. Maximum runner count not reached

**Resolution**: Verify Puppet configuration applied and service restarted

---

## Next Steps

- **Optimize resources**: Profile your workflows to right-size runner resources
- **Implement monitoring**: Set up Prometheus alerts for queue depth and runner health
- **Plan production**: Use staging metrics to size production runner pool (see ADR-0002)

## Related Documentation

- [Reference: Forgejo Configuration](../reference/forgejo-config.md)
- [Explanation: Actions Scalability Strategy (ADR-0002)](../../ADR/0002-actions-scalability.md)
- [How-To: Puppet Tasks](puppet-tasks.md)
