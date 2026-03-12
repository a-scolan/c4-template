Start top-down, not bottom-up.

1. Begin with **C1 Context**: define the system boundary, the main actors, and external systems.
2. Move to **C2 Containers**: split the system into the runtime building blocks that make it work and show their main interactions.
3. Add **C3 Components** only **selectively**: use it only for containers that are complex, risky, or architecturally central.

After the structural model is stable, you can add two optional layers:

- **Dynamic views** in `views 'Use Cases'` when a workflow needs time-ordered steps.
- **Deployment views** when runtime topology, environments, zones, or instances matter.

So the core path is **C1 → C2 → C3**, with **Dynamic** and **Deployment** as optional follow-ups when they add real value. Avoid starting from classes, folders, or framework details.