You should treat this as an ADR-worthy architecture decision. Here is a clean way to frame the ADR.

# ADR: Choose PostgreSQL over MongoDB for Main Database Container

## Status
Proposed (or Accepted, if already decided)

## Context
Our main database container must support transactional consistency, strong data integrity, and complex relational queries across core business entities. We evaluated PostgreSQL and MongoDB as primary data stores.

## Decision Drivers
- Strong ACID transaction guarantees for core workflows
- Relational modeling and referential integrity
- Predictable query performance for joins and reporting
- Operational maturity, backup/restore tooling, and observability
- Team expertise and lower long-term operational risk

## Options Considered
1. PostgreSQL as primary database
2. MongoDB as primary database

## Decision
We choose **PostgreSQL** as the primary database for the main container.

## Rationale
PostgreSQL aligns better with our consistency and relational requirements. It provides first-class transactions, schema constraints, and robust SQL capabilities that reduce application-level complexity for core domain logic.

## Consequences
### Positive
- Strong consistency and integrity for critical data
- Simpler enforcement of business invariants at the data layer
- Rich SQL ecosystem for analytics and ad hoc diagnostics

### Negative / Trade-offs
- Less flexible for rapidly changing unstructured schemas
- Potential impedance mismatch for document-heavy use cases

## Risk Mitigations
- Use JSONB selectively for semi-structured fields
- Apply migration tooling and schema review process
- Define indexing/query standards and performance budgets

## Follow-up
- Finalize data model and migration plan
- Define backup, retention, and restore SLAs
- Add runbooks for scaling, failover, and incident response
