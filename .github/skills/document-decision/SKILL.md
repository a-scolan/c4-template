---
name: document-decision
description: Use when recording WHY architectural choices were made (technology selection, pattern decisions, infrastructure design). Captures context, trade-offs, and consequences using standard ADR format.
---

# Document Architecture Decision

## Overview

Creates Architecture Decision Records (ADRs) to capture WHY architectural choices were made in a LikeC4-modeled system. Uses standard ADR format: Status, Context, Decision, Consequences. Stored in `ADR/NNNN-decision-title.md`.

## When to Use

- Selecting a technology for a container or system (Kong vs HAProxy, MongoDB vs PostgreSQL)
- Choosing an architectural pattern (async processing, microservices, CQRS)
- Making a deployment infrastructure decision (VM sizing, replication strategy, zone topology)
- Any decision whose rationale would be unclear six months from now

**Do not use** for repository tooling, CI/CD setup, or LikeC4 modeling process decisions.

## Quick Reference

| Field | Content |
|-------|---------|
| **Filename** | `ADR/NNNN-decision-title.md` (manually increment NNNN) |
| **Template** | `ADR/0000-template.md` |
| **Status** | Proposed / Accepted / Deprecated / Superseded |
| **Sections** | Context → Decision → Consequences (Positive / Negative / Neutral) |

## Scope

- ✅ System design decisions (why Kong API Gateway vs HAProxy, why MongoDB vs PostgreSQL)
- ✅ Container-level technology choices (why RabbitMQ for queuing, why MinIO for storage)
- ✅ Component architecture patterns (why async processing, why microservices)
- ✅ Deployment infrastructure choices (why 3-node replication, why specific VM sizing)
- ❌ NOT repository structure, tooling, CI/CD setup, or LikeC4 modeling decisions

## Example

```markdown
# ADR-0001: API Gateway Selection - Kong vs HAProxy

## Status
Accepted

## Context
Legacy system used HAProxy as a simple load balancer. Microservices architecture requires:
- API-aware routing based on paths, headers, JWT claims
- Built-in authentication (JWT validation, OAuth2)
- Rate limiting and circuit breakers
- Plugin ecosystem for extensibility

## Decision
Upgrade from HAProxy to Kong API Gateway

## Consequences

### Positive
- Routes to multiple backend services with path-based rules
- JWT validation out-of-the-box, reducing custom auth code
- Production-grade rate limiting without custom implementation
- Extensible via Lua plugins

### Negative
- More complex configuration than HAProxy
- Requires learning Kong admin API and declarative config
- Higher resource footprint (but acceptable for use case)
```

## Common Mistakes

❌ **Documenting HOW the model was built** — ADRs capture WHY a design choice was made, not how to use LikeC4

❌ **Missing Context section** — without context the decision is meaningless in the future; always explain what constraints drove it

❌ **Only Positive consequences** — every real decision has trade-offs; omitting negatives makes the ADR incomplete and less trustworthy

❌ **Wrong filename format** — use `ADR/NNNN-title.md` with leading zeros (0001, 0002, ...), not arbitrary filenames

## Integration with LikeC4

- Reference elements from diagrams: "The decision affects `mySystem.apiGateway` (Container_ReverseProxy)"
- Link to views: "See deployment view: `deployment_api_tier`"
- Tag related decisions: Use frontmatter or Notes section to link ADRs
