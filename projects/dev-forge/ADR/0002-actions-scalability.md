# ADR-0002: Forgejo Actions Scalability Strategy

## Status

Accepted

## Context

Dev-Forge's CI/CD system (Forgejo Actions) must scale to support development teams without degrading performance or reliability. Key considerations:

**Workload Characteristics**:
- Variable demand: Low overnight, high during business hours
- Unpredictable spikes: Large merge, many simultaneous pushes
- Diverse workflows: Quick linting (< 1 min) to heavy builds (30+ min)
- Technology variety: Different languages require different environments

**Constraints**:
- On-premises infrastructure (no cloud auto-scaling)
- Budget limitations on VM provisioning
- Developer expectation: CI/CD results within 5 minutes for typical workflows
- Staging environment must validate production architecture

**Current Situation**:
- No CI/CD infrastructure deployed
- Staging environment is first deployment target
- Must demonstrate scalability before production rollout

### Alternatives Considered

**Static Runner Pool (No Auto-Scaling)**:
- ✅ Simple configuration
- ✅ Predictable resource usage
- ❌ Over-provision for peak load (waste during low usage)
- ❌ Under-provision risks queueing and delays
- ❌ Cannot adapt to organic growth

**Over-Provisioned Static Pool**:
- ✅ Always capacity available
- ❌ Significant resource waste (70-80% idle most of time)
- ❌ High infrastructure cost
- ❌ Does not scale beyond initial provisioning

**Kubernetes-Based Auto-Scaling**:
- ✅ Cloud-native scaling patterns
- ✅ Fine-grained resource allocation
- ❌ Requires Kubernetes cluster (additional operational complexity)
- ❌ Overhead for small/medium scale
- ❌ Team unfamiliarity with Kubernetes operations

**External CI/CD Service (GitHub Actions, GitLab SaaS)**:
- ✅ Unlimited scaling
- ✅ No infrastructure management
- ❌ Contradicts on-premises requirement
- ❌ Data sovereignty concerns
- ❌ Requires outbound internet connectivity
- ❌ Recurring costs per minute of usage

## Decision

We will implement a **containerized runner pool with queue-based auto-scaling**:

### Architecture

**Base Runner Pool**: 2 always-running runners (staging environment)
- Provides immediate availability for functional validation testing
- Minimal baseline ensures staging remains cost-effective
- Not sized for performance testing—staging validates platform functionality, NOT production capacity

**Auto-Scaling Controller**:
- Monitors Forgejo Actions queue depth every 30 seconds
- Scales up when queue depth > 2 (more workflows waiting than running)
- Scales down after 5 minutes of runner idle time (faster deprovisioning for cost efficiency)
- Maximum: 10 concurrent runners (staging), 25 (production)

**Runner Configuration**:
- Docker-based execution (containerized workflows)
- Resource allocation: 2 vCPU, 4 GB RAM per runner (standard)
- High-memory variant: 4 vCPU, 8 GB RAM (for heavy builds)
- Ephemeral runners: Destroyed after job completion (clean state)

### Scaling Logic

```
if queue_depth > scale_up_threshold:
    active_runners < max_runners:
        provision_new_runner()

if runner_idle_time > scale_down_delay:
    active_runners > base_runner_count:
        decommission_runner()
```

**Parameters**:
- `base_runner_count`: 2 (staging), 8 (production planned)
- `max_runner_count`: 10 (staging), 25 (production planned)
- `scale_up_threshold`: 2 workflows waiting
- `scale_down_delay`: 5 minutes idle
- `scaling_check_interval`: 30 seconds

### Implementation

- **Puppet-managed**: Runner pool configuration in Puppet manifests
- **VM-based**: Each runner is a lightweight VM (fast provisioning ~30-60 seconds)
- **Registration**: Runners auto-register with Forgejo on startup
- **Monitoring**: Prometheus metrics expose queue depth, runner utilization

## Consequences

### Positive Consequences

- **Cost-Efficient**: Only pay for VMs actively running workflows
- **Responsive**: Auto-scaling reacts within 1-2 minutes of demand spike
- **Predictable**: Base pool ensures no cold-start delays for typical workflows
- **Graceful Degradation**: Queue system provides natural backpressure
- **Technology-Agnostic**: Containerized execution supports any language/framework
- **Validated in Staging**: Staging environment proves scalability before production
- **Observable**: Metrics enable data-driven capacity planning

### Negative Consequences

- **Complexity**: Auto-scaling logic adds operational complexity vs static pool
- **Provisioning Delay**: 30-60 second lag between demand spike and runner availability
- **Resource Overhead**: Container and VM overhead (vs bare-metal runners)
- **Monitoring Required**: Must actively monitor queue and adjust thresholds
- **Puppet Dependency**: Scaling tightly coupled to Puppet automation

### Neutral Consequences

- **VM Management**: Requires VM lifecycle management (provisioning, decommissioning)
- **Runner Labels**: Need strategy for matching workflows to runner types (standard, high-memory)
- **State Management**: Ephemeral runners simplify cleanup but prevent caching (trade-off)

## Notes

### Staging Validation

**Staging Purpose**: Functional validation of Dev-Forge platform deployment and configuration, NOT performance testing.

Staging verifies:
1. Runner provisioning and auto-scaling logic functions correctly
2. Workflows execute successfully with proper authentication
3. Artifact storage and retrieval works as expected
4. Integration with Forgejo web UI is seamless
5. Puppet automation correctly manages runner lifecycle

**Important**: Staging is deliberately undersized (2 base runners) to minimize cost. Performance metrics and production capacity planning MUST be validated in actual production use with real project workloads, as synthetic load testing in staging would not represent real usage patterns.

### Production Sizing

**Initial Production Parameters** (to be adjusted based on actual usage):
- `base_runner_count`: 8 (conservative initial estimate, monitor and adjust)
- `max_runner_count`: 25 (allows significant burst capacity)

**Production Tuning Strategy**:
- Monitor queue depth, wait times, and runner utilization for first 30 days
- Adjust `base_runner_count` targeting 50-70% baseline utilization
- Adjust `max_runner_count` ensuring peak load never saturates (keep 20% headroom)
- Review metrics monthly and tune parameters based on observed patterns

### Alternative Scaling Triggers

Future enhancements could scale based on:
- Time of day (more runners during business hours)
- Team size (automatic adjustment as developers join)
- Workflow duration prediction (pre-scale for known heavy builds)

### Related Decisions

- [ADR-0001: Forgejo Platform](0001-forgejo-platform.md) — Platform provides native Actions support
- [ADR-0003: Puppet Automation](0003-puppet-automation.md) — Puppet orchestrates runner provisioning
- [ADR-0006: Technology Neutrality](0006-tech-neutrality.md) — Container-based execution enables language independence

### References

- GitHub Actions Scaling Patterns: https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/autoscaling-with-self-hosted-runners
- Forgejo Actions Documentation: https://forgejo.org/docs/next/user/actions/
- Internal capacity planning spreadsheet (Confluence: "Dev-Forge Capacity")
