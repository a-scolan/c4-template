Use `understand-project-structure` first.

Then choose a **future-state rich description** format (short but structured), in this order:
1. **Intent** (what this service/VM will do)
2. **Scope** (what is in/out)
3. **Operational contract** (availability, security, monitoring, backup)
4. **Dependencies** (network, storage, upstream/downstream)
5. **Assumptions & TBDs** (explicit unknowns)

Because the element does not exist yet, avoid fake implementation details. Mark unknowns as `TBD` instead of guessing.