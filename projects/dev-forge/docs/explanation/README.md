# Explanation: Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) documenting significant decisions made during the design and implementation of the Dev-Forge platform.

---

## What are ADRs?

Architecture Decision Records capture the **why** behind architectural choices. They document:
- The context and forces that led to a decision
- The decision itself and its rationale
- The consequences (positive, negative, and neutral) of that choice

---

## ADR Index

### Platform & Technology Selection

- **[ADR-0001: Forgejo Platform Selection](0001-forgejo-platform.md)**  
  Why we chose Forgejo over GitLab, Gitea, and other Git hosting platforms

- **[ADR-0003: Puppet for Infrastructure Automation](0003-puppet-automation.md)**  
  Why we selected Puppet for configuration management and deployment orchestration

- **[ADR-0007: Nexus Registry Integration](0007-nexus-integration.md)**  
  Why we integrate with existing Nexus instead of using Forgejo's native registry

### Scalability & Architecture

- **[ADR-0002: Actions Scalability Strategy](0002-actions-scalability.md)**  
  Runner pool architecture and auto-scaling design for CI/CD workloads

- **[ADR-0005: Network Zone Architecture](0005-network-zones.md)**  
  Network segmentation strategy (DMZ, AppTier, DataTier) and security boundaries

### Features & Functionality

- **[ADR-0004: MVP Plugin Selection](0004-mvp-plugins.md)**  
  Five essential plugins for initial deployment (auth, actions, repos, registry, code review)

- **[ADR-0006: Technology Neutrality Principle](0006-tech-neutrality.md)**  
  Platform design to support any programming language or framework

---

## ADR Lifecycle

ADRs follow these statuses:

- **Proposed**: Under consideration and discussion
- **Accepted**: Decision made and being implemented
- **Deprecated**: No longer recommended but not yet replaced
- **Superseded**: Replaced by a newer ADR (reference included)

Each ADR includes its current status at the top of the document.

---

## When to Create an ADR

Create an ADR when making decisions about:
- ✅ Technology selection (databases, frameworks, platforms)
- ✅ Architectural patterns (microservices, event-driven, etc.)
- ✅ Infrastructure design (network topology, scaling strategies)
- ✅ Security and compliance approaches
- ✅ Integration patterns with external systems

Do **not** create ADRs for:
- ❌ Implementation details (those go in code comments or how-to guides)
- ❌ Temporary workarounds
- ❌ Routine configuration changes
- ❌ Bug fixes

---

## ADR Template

New ADRs should follow the [template structure](../template/ADR/0000-template.md):

```markdown
# ADR-NNNN: Title

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
[Why is this decision needed? What forces are at play?]

## Decision
[What are we doing and why?]

## Consequences
### Positive
[Benefits and improvements]

### Negative
[Trade-offs and limitations]

### Neutral
[Notable changes that are neither clearly positive nor negative]
```

---

## Contributing to ADRs

1. **Propose**: Create draft ADR with "Proposed" status
2. **Discuss**: Share with stakeholders for feedback
3. **Decide**: Update status to "Accepted" when decision is made
4. **Implement**: Reference ADR in implementation work
5. **Update**: Mark as "Deprecated" or "Superseded" if decision changes

---

## Related Documentation

- [Tutorials](../docs/tutorial/) — Learn by doing
- [How-To Guides](../docs/how-to/) — Practical task completion
- [Reference](../docs/reference/) — Technical specifications

ADRs complement these by explaining the **rationale** behind what you're learning, doing, or referencing.
