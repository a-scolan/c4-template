Start top-down, not code-first.

1. **C1 — Context first**
   - Define the system boundary.
   - Identify the main users, external systems, and the key static relationships around the product.
   - Keep this at the business/context level.

2. **C2 — Containers next**
   - Break the SaaS product into its major runtime pieces: web app, API, worker, database, queue, external dependencies, and so on.
   - Show the main responsibilities and relationships between those containers.

3. **C3 — Components only where needed**
   - Go inside a container only if its internal structure is important to explain.
   - Use C3 selectively for containers that are complex, critical, risky, or hard to understand from C2 alone.

4. **Optional views after the core static model**
   - **Deployment** is optional and should be added when runtime/infrastructure placement matters.
   - **Dynamic / use-case views** are optional and should be added when you need to show time-ordered behavior or scenarios.

A practical rule is: establish the static story first with **C1 → C2**, then add **C3** only where it genuinely adds clarity. Stop at C2 if the system is simple enough there.