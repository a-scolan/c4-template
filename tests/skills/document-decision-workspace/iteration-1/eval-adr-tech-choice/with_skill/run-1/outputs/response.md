Oui. Pour ce choix PostgreSQL vs MongoDB, écris un ADR séparé, par exemple `projects/template/ADR/0001-postgresql-over-mongodb.md`.

Structure minimale :
- Status
- Context
- Decision
- Consequences

Dans le Context, explicite les besoins transactionnels autour de `mySystem.database`.
Dans la Decision, formule clairement `PostgreSQL plutôt que MongoDB`.
Dans les Consequences, note les plus et les moins : garanties relationnelles, mais schéma plus rigide et migrations à gérer.
