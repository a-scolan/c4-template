Suggested ADR file: `ADR/0001-use-postgresql-for-main-database.md`

## Status

Proposed

## Context

We are choosing the primary persistence technology for the system’s main database container. The current option under discussion is MongoDB, but the system appears to need stronger transactional guarantees, clearer relational modeling, and more predictable query behavior for core business data.

The decision affects more than the database container itself. It also impacts:
- the main database element in the LikeC4 model (for example `mainDatabase`)
- the calling service(s) that read and write core data (for example an API or domain service container)
- container/component views that show persistence technology and integration boundaries
- operational follow-up such as backups, migrations, replication, monitoring, and schema management

Key forces to capture in the ADR:
- need for ACID transactions and referential integrity
- reporting/query requirements across related entities
- team familiarity with relational tooling
- deployment and operational maturity for the chosen database
- cost of changing data access patterns and migration tooling

## Decision

Adopt PostgreSQL as the technology for the main database container instead of MongoDB.

Frame the decision explicitly around the impacted LikeC4 elements:
- update the main database container technology to PostgreSQL
- identify the primary calling service(s) that will depend on relational schema design, SQL queries, and migrations
- note any affected views where the technology label, relationship notes, or operational annotations should change

State the rationale clearly:
- PostgreSQL is a better fit for strongly related business data
- transactional consistency is more important here than flexible document storage
- the platform can still use features such as JSONB when some payloads are semi-structured

## Consequences

### Positive Consequences
- Stronger transactional guarantees for the system’s core data flows
- Better support for relational queries, joins, constraints, and data integrity rules
- Mature ecosystem for migrations, backups, replication, and observability
- Easier alignment between business invariants and the storage model for the calling service(s)

### Negative Consequences
- Less flexibility for highly variable document-shaped data than MongoDB
- Additional upfront schema design and migration discipline
- Potential rewrite of repository/query code in the calling service(s)
- Possible performance tuning work for indexing, query plans, and connection pooling

### Neutral Consequences
- LikeC4 views and element descriptions should be updated to reflect the new technology choice
- Operational ownership may shift toward SQL-focused runbooks, monitoring, and backup validation

A useful closing section in the ADR is “Follow-up work”, for example:
- add migration tooling and schema versioning
- update the database element and dependent service descriptions in the model
- revise persistence-related views and operational documentation
- validate backup/restore and high-availability expectations for PostgreSQL
