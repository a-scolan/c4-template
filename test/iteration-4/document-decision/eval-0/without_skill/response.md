Yes. This is ADR-worthy because it changes the main persistence technology for a core container.
Suggested ADR frame:
- Title: Use PostgreSQL instead of MongoDB for the main database container
- Status: Proposed
- Context: The main database must support core transactional workflows, reliable data integrity, reporting/query flexibility, operational maturity, and predictable schema evolution.
- Decision: Adopt PostgreSQL as the primary system-of-record database for the main container, and do not use MongoDB for this role.
- Key drivers: ACID transactions, referential integrity, strong consistency, SQL querying/reporting, mature backup/replication tooling, and team familiarity.
- Alternatives considered: MongoDB for schema flexibility and document-oriented modeling.
- Consequences: Better transactional safety, clearer schema governance, and easier relational querying; trade-offs include less document-model flexibility and different scaling patterns than MongoDB.
- Notes to include: expected data model shape, migration implications, operational assumptions, and any cases where document storage may still be used elsewhere.
