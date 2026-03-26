# ADR Outline — Select PostgreSQL over MongoDB for Core Persistence

## Proposed ADR filename
`ADR/0001-postgresql-primary-store-for-core-transactions.md`

## Status
Accepted

## Context
The core data store supports transactional business workflows with strict consistency needs. We compared MongoDB and PostgreSQL for the primary database container.

Decision forces:
- Transaction safety across multi-entity writes
- Strong need for relational integrity and SQL querying
- Predictable backup/restore and high-availability patterns
- Team operational maturity with PostgreSQL ecosystem

## Decision
Choose **PostgreSQL** for the main transactional database container.

Explicitly not decided here:
- Non-transactional analytics lake choices
- Event/document side stores for specialized workloads

## Impacted Elements
- Core backend/API service container
- Primary database container (technology: PostgreSQL)
- Repository/data-access components and migration pipeline
- Relevant architecture/deployment views that document persistence and resilience

## Alternatives Considered
### MongoDB
- Benefit: flexible schema evolution
- Drawback: weaker fit for relational constraints and join-heavy operational reporting in this domain

### PostgreSQL (chosen)
- Benefit: ACID semantics, rich relational model, mature ops tooling
- Drawback: schema governance and migration discipline are mandatory

## Consequences
### Positive
- Reliable transactional behavior for critical paths
- Better alignment with relational analytics/reporting needs
- Mature HA and disaster-recovery playbooks

### Negative
- Increased rigor for schema changes and release sequencing
- Potential operational tuning costs under heavy write load

### Neutral
- Some document-shaped payload handling can remain in boundary adapters or caches

## Follow-up
- Set the database container technology to `PostgreSQL`
- Define migration conventions and rollback policy
- Verify persistence and failover assumptions in deployment docs/views
- Capture backup, restore, and replication SLO/SLA expectations
