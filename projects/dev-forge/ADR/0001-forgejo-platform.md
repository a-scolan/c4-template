# ADR-0001: Forgejo Platform Selection

## Status

Accepted

## Context

Dev-Forge requires a self-hosted Git platform that provides:
- Git hosting and management (core requirement)
- CI/CD automation capabilities
- Code review and collaboration tools
- On-premises deployment (organizational requirement)
- Package registry integration
- Technology-agnostic support (any language/framework)
- Reasonable resource footprint
- Active development and community

### Alternatives Considered

**GitLab Community Edition**:
- ✅ Feature-rich, mature platform
- ✅ Strong CI/CD (GitLab CI)
- ✅ Integrated container registry
- ❌ Heavy resource requirements (8 GB RAM minimum)
- ❌ Complex architecture (multiple services)
- ❌ **Complex maintenance and update procedures** (multi-step upgrades, database migrations, service orchestration)
- ❌ Slower performance on modest hardware
- ❌ Community Edition limitations (some features Enterprise-only)

**Gitea**:
- ✅ Lightweight, fast performance
- ✅ Simple deployment (single binary)
- ✅ Low resource requirements
- ✅ Similar UI/UX to GitHub
- ⚠️ Limited CI/CD (Gitea Actions just emerging)
- ⚠️ Smaller community than GitLab
- Note: Forgejo is a Gitea soft fork

**GitHub Enterprise Server**:
- ✅ Industry standard, familiar to developers
- ✅ Excellent Actions CI/CD
- ✅ Best-in-class code review experience
- ❌ Proprietary, closed-source
- ❌ Expensive licensing
- ❌ Requires constant internet connectivity for updates
- ❌ Limited customization options

**BitBucket Server/Data Center**:
- ✅ Atlassian integration (Jira, Confluence)
- ✅ Mature code review (pull requests)
- ❌ Expensive Atlassian licensing
- ❌ Java-based (higher resource usage)
- ❌ CI/CD requires separate Bamboo installation
- ❌ Less active open-source community

### Key Requirements Matrix

| Requirement | GitLab CE | Gitea | Forgejo | GitHub Ent | BitBucket |
|-------------|-----------|-------|---------|------------|-----------|
| On-premises | ✅ | ✅ | ✅ | ✅ | ✅ |
| Open source | ✅ | ✅ | ✅ | ❌ | ❌ |
| Lightweight | ❌ | ✅ | ✅ | ❌ | ❌ |
| CI/CD native | ✅ | ⚠️ | ✅ | ✅ | ❌ |
| Active dev | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| Cost | Free | Free | Free | $$$$ | $$$$ |

## Decision

We will adopt **Forgejo** as the Dev-Forge Git platform.

### Rationale

1. **Already in Use**: Organizational teams are familiar with Forgejo, reducing training overhead

2. **Resource Efficiency**: Runs well on modest hardware (2 GB RAM, 2 vCPU), enabling cost-effective scaling

3. **Integrated CI/CD**: Forgejo Actions provides GitHub Actions-compatible workflows without additional tooling

4. **Open Source Governance**: Community-driven fork ensures transparency and avoids vendor lock-in

5. **Active Development**: Regular releases, responsive maintainers, growing ecosystem

6. **Migration Path**: Compatible with Gitea, provides upgrade path if needed

7. **Technology Neutrality**: No language/framework bias—supports all ecosystems equally

### Why Not Others

**GitLab**: Resource overhead (8+ GB RAM) incompatible with target infrastructure budget, and critically, complex maintenance/update procedures requiring multi-step migrations and service orchestration add unacceptable operational burden

**Gitea**: Forgejo offers same benefits plus stronger commitment to open-source governance

**GitHub Enterprise**: Proprietary licensing and costs unjustified for on-premises use case

## Consequences

### Positive Consequences

- **Familiar Interface**: Teams already experienced with Forgejo UI/workflows
- **Fast Performance**: Lightweight Go binary ensures responsive experience
- **Simple Operations**: Single binary simplifies deployment, updates, and debugging
- **Cost-Effective**: No licensing costs, modest infrastructure requirements
- **Community-Driven**: Open governance model aligns with organizational values
- **Actions Compatibility**: Can leverage existing GitHub Actions knowledge and workflows
- **Future-Proof**: Active community development ensures ongoing improvements

### Negative Consequences

- **Smaller Ecosystem**: Fewer integrations and plugins compared to GitLab or GitHub
- **Feature Maturity**: Some advanced features less mature than GitLab equivalents
- **Community Size**: Smaller community means fewer Stack Overflow answers/tutorials
- **Commercial Support**: Limited paid support options compared to enterprise platforms
- **Perception**: Less recognized brand name compared to GitHub/GitLab

### Neutral Consequences

- **Soft Fork Dynamics**: Must monitor Gitea/Forgejo relationship for potential divergence
- **Learning Curve**: New developers unfamiliar with Forgejo need onboarding (mitigated by similarity to GitHub)
- **Integration Work**: May need custom integrations for organizational tools

## Notes

### Migration Considerations

Forgejo supports import from:
- GitHub (repositories, issues, pull requests)
- GitLab
- Gitea
- Generic Git repositories

This enables gradual migration of existing repositories if needed.

### Related Decisions

- [ADR-0002: Actions Scalability](0002-actions-scalability.md) — CI/CD runner architecture
- [ADR-0004: MVP Plugins](0004-mvp-plugins.md) — Essential platform features

### Review Criteria

This decision should be reviewed if:
- Community development stalls (no releases for 12+ months)
- Critical security issue unpatched for 6+ months
- Performance degrades significantly at scale
- Gitea/Forgejo divergence creates significant compatibility issues

### References

- Forgejo Official Documentation: https://forgejo.org/docs/
- Forgejo vs Gitea Comparison: https://forgejo.org/compare-to-gitea/
- GitLab System Requirements: https://docs.gitlab.com/ee/install/requirements.html
- Internal team feedback (Confluence: "Git Platform Evaluation")
