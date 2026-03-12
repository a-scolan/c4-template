Suggested ADR file: `ADR/0007-choose-postgresql-for-primary-database.md`

# ADR: Choose PostgreSQL for the main database container

## Status
Proposed

## Context
The system’s main database container must support transactional business workflows, consistent writes, relational querying, backup/restore procedures, and predictable operational practices. The current choice is between PostgreSQL and MongoDB for the primary persistence layer.

This decision affects more than the database itself. At minimum, capture the impacted scopes explicitly:
- the main database container (use its real LikeC4 element ID or stable name)
- the calling service or API that owns reads/writes to that database
- any persistence, backup, failover, or deployment views that document the data layer

## Decision
Use PostgreSQL for the main database container as the primary transactional store.

MongoDB is not selected for this container. If document-style storage is still useful later, treat that as a separate decision for a separate bounded use case rather than folding it into the primary transactional store.

## Consequences

### Positive
- Strong ACID guarantees for core transactional workflows
- Clear fit for relational data, joins, and reporting needs
- Mature ecosystem for backups, replication, migrations, and observability
- Broad operational familiarity and predictable administration practices

### Negative
- Requires schema migration discipline and versioned database changes
- Less flexible than a document database for rapidly changing payload shapes
- Operational tuning may be needed as write volume and query complexity grow
- Teams must be deliberate about modeling data instead of relying on schema drift

### Follow-up
- Update the database container technology to `PostgreSQL`
- Identify the calling service(s) or API(s) that must adjust queries, migrations, or ORM settings
- Review backup, restore, replication, and failover assumptions in deployment documentation
- Validate any LikeC4 views that show persistence, data ownership, or operational recovery
- If needed, add an `Alternatives Considered` section summarizing why MongoDB was rejected for this primary role
