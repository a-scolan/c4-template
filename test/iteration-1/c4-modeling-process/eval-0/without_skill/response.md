Start top-down, not bottom-up.

1. **C1 first**: define the system boundary, primary users, and external systems.
2. **C2 next**: break the system into its main containers and show their responsibilities and relationships.
3. **C3 only where needed**: zoom into a container’s internal components when that extra detail is useful.

What is optional:
- **Deployment views** are optional and should be added only when infrastructure or runtime placement matters.
- **Dynamic / use-case views** are optional and should be added only when a scenario or sequence of interactions needs to be explained.

So the core path is **C1 → C2 → selective C3**, with deployment and dynamic views added later only for targeted needs. Avoid starting from code, classes, or low-level implementation details.