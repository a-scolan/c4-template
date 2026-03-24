Yes — this is a good fit for an ADR. Frame it as a lasting architecture choice, not just a database preference.

Suggested ADR structure:

# Choose PostgreSQL for the primary transactional database

## Status
Accepted (or Proposed, if still under review)

## Context
- The system’s main database container must support transactional consistency, structured querying, backups, and predictable operations.
- The decision is between PostgreSQL and MongoDB for the primary store.
- Capture the forces that matter: data integrity, query patterns, reporting needs, schema evolution, team familiarity, backup/replication tooling, and expected scale.

## Decision
Use PostgreSQL for the main database container.
State exactly where it applies, for example: use PostgreSQL for the real primary database element in the model. Also state what is out of scope, such as analytics stores, caches, or any document-oriented side store.

## Impacted Elements
List the real affected elements, such as:
- the application/API container(s) that read and write business data
- the primary database container
- any deployment or documentation slice that covers persistence, backup, or failover
Do not invent element IDs; use the actual model identifiers if they are known.

## Alternatives Considered
- MongoDB: flexible document model and easy schema evolution, but a weaker fit if the main workload needs strict transactions, joins, and relational reporting.
- PostgreSQL: stronger ACID guarantees and a mature operational ecosystem, but it requires schema migration discipline.

## Consequences
### Positive
- Strong transactional guarantees for core workflows
- Mature backup, replication, and observability ecosystem
- Better fit for relational queries, joins, and reporting

### Negative
- Requires schema design and migration discipline
- Less convenient for rapidly changing document-shaped payloads
- May need operational tuning as write volume grows

### Neutral
- JSON-heavy edge cases may still be handled in adapters or side patterns if needed

## Follow-up
- Update the database container technology to PostgreSQL
- Review backup, replication, and failover assumptions
- Recheck any views or documentation that describe persistence

A strong one-line title would be: Choose PostgreSQL for the primary transactional database.
