# ADR Draft Structure — PostgreSQL as Primary DB (instead of MongoDB)

## File suggestion
`ADR/0001-postgresql-as-primary-transactional-database.md`

## Status
Accepted

## Context
The primary database underpins mission-critical transactional workflows. We need strong consistency, referential integrity, and robust operational recovery. MongoDB and PostgreSQL were evaluated for this primary role.

Constraints and drivers:
- Multi-step transactions with strict correctness expectations
- Relational model and query patterns (joins, constraints, reporting)
- Mature backup/replication/failover ecosystem
- Team capability in SQL-based schema evolution

## Decision
Standardize on **PostgreSQL** for the main database container.

Scope boundaries:
- This does not prohibit document-oriented storage for secondary/specialized use cases
- This ADR governs the primary transactional store only

## Impacted Elements
- Core service/API container interacting with transactional data
- Main database container (technology value becomes PostgreSQL)
- Data access layer components and migration toolchain
- Related architecture/deployment views discussing persistence and DR

## Alternatives Considered
### MongoDB (not selected for this use case)
- Advantage: flexible schema model
- Trade-off: less natural fit for relational constraints and join-centric workflows

### PostgreSQL (selected)
- Advantage: ACID, relational fidelity, operational maturity
- Trade-off: schema migration governance required

## Consequences
### Positive
- Strong transactional guarantees and integrity controls
- Better fit for relational reporting/querying
- Proven operational practices for backup, replication, recovery

### Negative
- Added process rigor for schema migration lifecycle
- Need continuous performance tuning as scale grows

### Neutral
- Document-heavy integration payloads can remain outside primary relational core

## Follow-up
- Update model technology for the primary DB container
- Define migration governance and rollback standards
- Validate persistence/failover assumptions in affected views/docs
- Align monitoring and capacity planning with PostgreSQL operations
