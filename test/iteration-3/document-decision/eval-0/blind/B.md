This is a good fit for an ADR. A sensible file path would be `ADR/0001-postgresql-primary-store.md`.

## Status
Proposed

## Context
The main database container must support transactional consistency, relational querying, mature backup and replication tooling, and predictable operations. The key alternatives are PostgreSQL and MongoDB. If the core business data is relational and the calling service depends on joins, constraints, and ACID behavior, PostgreSQL is the stronger fit for the primary store.

## Decision
Use PostgreSQL for the main database container, for example `yourSystem.primaryDatabase`, and do not use MongoDB as the primary transactional store. This decision also affects the service that reads and writes that database, for example `yourSystem.api`, plus any views or deployment documentation that describe persistence, backup, failover, or schema migration.

## Impacted Elements
- Primary database container: `yourSystem.primaryDatabase`
- Calling service or API: `yourSystem.api`
- Any context/container/deployment views that show the application-to-database relationship
- Operational documentation for backup, restore, replication, and migrations

## Consequences
### Positive
- Strong ACID guarantees for transactional workflows
- Mature ecosystem for replication, backup, monitoring, and schema migration
- Clear fit for relational reporting and integrity constraints

### Negative
- Requires schema migration discipline and versioning
- Less natural fit for highly variable document-shaped payloads
- Operational tuning may be needed as write volume grows

## Follow-up
- Update the database container technology to PostgreSQL
- Review backup, replication, and restore assumptions
- Validate affected views that show the API-to-database relationship
- Capture migration and operational ownership changes in supporting documentation
