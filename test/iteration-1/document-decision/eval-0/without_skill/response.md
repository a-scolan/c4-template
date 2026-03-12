You can frame the ADR like this.

Suggested file: `ADR/0001-use-postgresql-for-mySystem-database.md`

# ADR-0001: Use PostgreSQL for `mySystem.database`

## Status

Proposed

## Context

The template currently models `mySystem.database` as the main data store for the system. We are deciding whether to standardize on PostgreSQL instead of MongoDB for this container.

Key drivers:
- The system exposes an API and persists application and user data.
- The data model is likely to benefit from strong consistency, relational queries, and schema control.
- The team wants a widely adopted, well understood operational model.
- We need a decision that fits the template’s container architecture and can be referenced from the LikeC4 model.

## Decision

Use PostgreSQL as the technology for `mySystem.database` instead of MongoDB.

Rationale:
- PostgreSQL is a strong fit for structured business data and transactional workloads.
- It supports relational modeling, joins, constraints, and mature indexing strategies.
- It simplifies enforcing data integrity in a system where the API is the central entry point.
- The decision keeps the container explicit in the model as `mySystem.database` while clarifying its intended role and technology choice.

## Consequences

### Positive Consequences
- Strong ACID guarantees for critical application data.
- Clear schema management and stronger data integrity constraints.
- Mature ecosystem for backups, migrations, monitoring, and operations.
- Easier reporting and ad hoc querying for relational data needs.

### Negative Consequences
- Less flexibility for highly variable or document-shaped data than MongoDB.
- Schema evolution requires more planning and migration discipline.
- Horizontal scaling patterns can be more complex depending on future load.
- Teams expecting document-first modeling may need to adapt their approach.

### Neutral Consequences
- The LikeC4 element remains `mySystem.database`; the main change is the recorded technology choice.
- Application code and deployment documentation may need follow-up updates to stay consistent with the ADR.

## Notes

### Related Elements
- `mySystem.database`
- `mySystem.api`

### References
- Template ADR: `projects/template/ADR/0000-template.md`
- LikeC4 model: `projects/template/system-model.c4`
