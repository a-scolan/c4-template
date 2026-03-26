# ADR Framing — PostgreSQL instead of MongoDB for the Main Database

## Suggested filename
`ADR/0001-choose-postgresql-for-primary-transactional-store.md`

## Status
Accepted

## Context
Our main database container supports core business transactions that require consistency, relational querying, and reliable recovery procedures. The team evaluated MongoDB and PostgreSQL for this role.

Key forces:
- Need strong transactional guarantees for multi-step business operations
- Relational data model with frequent joins and reporting queries
- Requirement for mature backup/restore and replication practices
- Existing team familiarity with SQL migration workflows

## Decision
Use **PostgreSQL** as the primary database technology for the main database container.

Out of scope:
- Replacing specialized document/event stores used for non-transactional workloads
- Immediate redesign of all read models

## Impacted Elements
- Main API/backend container that reads/writes transactional data
- Main database container (technology set to PostgreSQL)
- Data access components/repositories in the application layer
- Any persistence/deployment views documenting backup, failover, or replication

## Alternatives Considered
### MongoDB (rejected for primary transactional store)
- Pros: flexible schema, fast iteration on document-shaped data
- Cons: weaker fit for relational integrity and join-heavy workflows in our core domain

### PostgreSQL (selected)
- Pros: ACID guarantees, strong relational model, mature operational tooling
- Cons: stricter schema migration discipline, tuning needed at scale

## Consequences
### Positive
- Better fit for transactional correctness and referential integrity
- Easier SQL-based analytics/reporting on core entities
- Mature ecosystem for HA, backup, observability, and operations

### Negative
- Requires disciplined schema/version migration process
- Potentially slower iteration when domain shape changes frequently
- Operational overhead for performance tuning and capacity planning

### Neutral
- Document-like payloads may still be handled at adapter or cache boundaries where appropriate

## Follow-up
- Update database container technology to `PostgreSQL` in the model
- Document replication, backup retention, and restore RTO/RPO assumptions
- Validate affected views and data-related relationships
- Add migration standards (DDL review, rollback strategy, release sequencing)
