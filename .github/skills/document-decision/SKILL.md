---
name: document-decision
description: Use when choosing or revisiting an architectural technology, integration boundary, deployment strategy, or cross-cutting pattern and you need to record the rationale, trade-offs, impacted LikeC4 elements, and consequences in an ADR.
---

# Document Architecture Decision

## Overview

Capture **why** an architectural choice was made, what alternatives were rejected, which modeled elements it affects, and what follow-up work it creates. An ADR should stay useful months later when the original discussion is gone.

Use the standard ADR backbone:
- **Status**
- **Context**
- **Decision**
- **Consequences**

Store ADRs as `ADR/NNNN-short-title.md`.

## When to Use

- Selecting a technology for a system, container, or component
- Choosing a boundary or interaction pattern (adapter, queue, webhook, SaaS replacement, CQRS)
- Making a deployment or resilience decision with long-term trade-offs
- Recording a decision whose rationale would otherwise be unclear later

**Do not use** for repository tooling, CI/CD setup, lint rules, or LikeC4 modeling workflow mechanics.

## Quick Reference

| Field | Guidance |
|-------|----------|
| **Filename** | `ADR/NNNN-short-title.md` with manually incremented leading zeros |
| **Core sections** | `Status / Context / Decision / Consequences` |
| **Recommended extras** | `Impacted Elements`, `Alternatives Considered`, `Follow-up` |
| **Starter template** | Use a local ADR starter if the workspace provides one, but adapt the content to the current decision |
| **Decision quality check** | Include both gains and costs, not just the preferred outcome |

## Scope

- ✅ Technology selection (`PostgreSQL` vs `MongoDB`, `Kong` vs `HAProxy`)
- ✅ Structural decisions (internal service vs SaaS, queue vs sync call, adapter boundaries)
- ✅ Infrastructure choices (replication, topology, managed vs self-hosted)
- ✅ Security/integration choices with lasting consequences
- ❌ Repository structure, CI/CD, editor tooling, or diagram-authoring mechanics

## Core Pattern

1. **Name the decision clearly** — one line that states the architectural choice.
2. **Capture the forces** — constraints, risks, scale, ownership, compliance, latency, migration pressure.
3. **State the decision** — what is chosen, where it applies, and what is explicitly out of scope.
4. **List impacted elements** — affected LikeC4 elements and, if useful, impacted views or deployment areas.
5. **Record consequences** — at least positive and negative, optionally neutral/operational consequences.
6. **Add follow-up** — migrations, model updates, validation, runbooks, or open questions.

## Example

```markdown
# ADR-0007: Choose PostgreSQL for the primary transactional store

## Status
Accepted

## Context
`{YourSystem}` needs strong transactional guarantees, relational querying, and predictable backup tooling.
The team considered MongoDB and PostgreSQL for the primary business data store.

## Decision
Use PostgreSQL for `{YourSystem}.primaryDatabase`.

## Impacted Elements
- `{YourSystem}.api`
- `{YourSystem}.primaryDatabase`
- Any view or deployment slice that documents persistence, backup, or failover

## Consequences

### Positive
- Strong ACID guarantees for transactional workflows
- Mature replication, backup, and observability ecosystem
- Clear fit for relational reporting and joins

### Negative
- Requires schema migration discipline
- Less flexible for rapidly changing document-shaped payloads
- Operational tuning may be needed as write volume grows

### Neutral
- Some JSON-heavy payloads may still remain in application-layer adapters

## Follow-up
- Update the database container technology to `PostgreSQL`
- Review replication and backup assumptions
- Validate affected views and deployment documentation
```

## Integration with LikeC4

- Reference impacted elements by **real element ID or stable descriptive name**
- Mention affected views only when they are known and relevant; do not invent view IDs
- If the decision changes the model itself, follow up with the appropriate modeling skill and then validate with `test-model`

Useful follow-ups:
- element or boundary changes → `create-element`, `create-relationship`
- deployment consequences → `model-deployment-infrastructure`
- validation after changes → `test-model`

## Common Mistakes

❌ **Documenting how the diagram was edited** — ADRs capture design rationale, not modeling mechanics

❌ **Missing costs or risks** — a decision without trade-offs reads like advocacy, not architecture

❌ **No impacted elements** — if readers cannot tell what parts of the model are affected, the ADR is too abstract

❌ **Confusing the ADR with an implementation checklist** — the ADR states the choice and its consequences; detailed execution can be follow-up work

❌ **Treating a local ADR starter as an oracle** — reuse the structure, not the example wording or domain content
