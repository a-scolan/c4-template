Use `ADR/0001-postgresql-over-mongodb.md`

# ADR-0001: Choose PostgreSQL for `mySystem.database`

## Status
Proposed

## Context
The template project needs a primary data store for `mySystem.database`. The expected workload favors strong consistency, relational integrity, structured reporting, and transactional updates across related entities. MongoDB was considered because of its flexible document model, but the current domain is better served by well-defined relationships, SQL querying, and predictable transactional behavior.

## Decision
Use PostgreSQL instead of MongoDB for `mySystem.database`.

## Consequences

### Positive
- Strong ACID transactions and referential integrity for core business data.
- SQL is a better fit for joins, reporting, and ad hoc analysis.
- Mature ecosystem for backups, replication, migrations, and observability.
- Schema constraints make data quality issues easier to prevent.

### Negative
- Less flexible than MongoDB for rapidly evolving document shapes.
- Schema evolution requires more upfront design and managed migrations.
- Horizontal scaling patterns can be more complex than in a document database approach.
- Teams expecting JSON-first modeling may lose some early development speed.