# Response — eval-0, without_skill, run 3

## Prompt

We're choosing PostgreSQL instead of MongoDB for the main database container in our system. Help me frame the ADR to write.

## Response

Here is a proposed ADR structure for the database technology decision:

---

**ADR-NNN: Use PostgreSQL Instead of MongoDB for the Main Database**

**Status:** Accepted

**Context:**

When designing the main database container, we considered two leading options:

| Attribute | PostgreSQL | MongoDB |
|-----------|-----------|---------|
| Model | Relational | Document |
| ACID | Full | Partial (per document) |
| Query Language | SQL | MQL |
| Schema | Strict | Flexible |
| Team familiarity | High | Medium |

The decision needed to account for the application's data model, consistency requirements, and long-term maintainability.

**Decision:**

We choose **PostgreSQL** as the primary relational database.

Our data has clearly defined relationships and benefits from referential integrity. The team is proficient with SQL. PostgreSQL's ACID compliance aligns with our consistency requirements. MongoDB's document model does not provide a meaningful advantage given our structured data access patterns.

**Consequences:**

*Positive:*
- Full ACID compliance for transactional operations
- Familiar SQL query language for the development team
- Strong support for complex joins and relational data integrity
- Wide ecosystem: migrations (Flyway), monitoring (pgAdmin, Prometheus exporter)

*Negative:*
- Schema changes require explicit migrations (no schema-free flexibility)
- Horizontal write scaling requires more complex configuration (e.g., Citus, partitioning)
- Vertical scaling may be needed before horizontal distribution

*Risks:*
- Future unstructured data use cases may require re-evaluation
- Consider MongoDB if requirements shift toward heavy document or hierarchical storage

---

Place this file in your project's `ADR/` folder following your numbering convention.
