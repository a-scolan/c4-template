# Response — eval-0, without_skill, run 2

## Prompt

We're choosing PostgreSQL instead of MongoDB for the main database container in our system. Help me frame the ADR to write.

## Response

To document this decision, I'll help you structure an Architecture Decision Record (ADR). Here's a framing for the PostgreSQL vs MongoDB choice:

---

**ADR: Choose PostgreSQL as the Primary Database**

**Status:** Accepted

**Context:**

The system requires a persistent data store for the main database container. We evaluated two candidate options:
- **MongoDB** — a document-oriented NoSQL database
- **PostgreSQL** — a relational SQL database with ACID compliance

The team needed to decide which best fits the data model, consistency requirements, and operational expertise.

**Decision:**

We will use **PostgreSQL** as the primary database container.

Reasons for this choice:
- The application data is inherently relational with clear schema constraints
- PostgreSQL provides strong ACID guarantees needed for transactional integrity
- The team has existing operational expertise with PostgreSQL
- Mature tooling ecosystem (migrations, ORMs, monitoring)
- Better support for complex ad-hoc queries via SQL

MongoDB was not selected because:
- The data model does not benefit significantly from a document store
- Schema flexibility is not a priority for this use case
- Team has less operational experience with MongoDB at scale

**Consequences:**

*Positive:*
- Strong data consistency guarantees
- SQL-based queries familiar to the engineering team
- Rich ecosystem of migration and schema management tools (Flyway, Liquibase)

*Negative:*
- Less flexible schema evolution compared to MongoDB
- Requires explicit schema migrations for structural changes
- Scaling requires more careful planning (read replicas, sharding)

---

Save this as `ADR-NNN-use-postgresql-database.md` in your ADR directory. Adjust the numbering to follow your existing ADR sequence.
