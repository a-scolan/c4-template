No—C3 is **not mandatory for every container**.

Use this decision rule:
- Stop at **C2** if the API container is simple and its purpose, interfaces, dependencies, and major responsibilities are already clear.
- Add **C3** only if that container is complex, critical, risky, or hard to understand without showing its internal parts.

Typical reasons to create C3 are:
- important internal components or workflows
- non-trivial security, orchestration, or domain logic
- performance-sensitive or failure-sensitive behavior
- a need to explain how the container is structured internally

So keep the progression **C1 → C2 → C3**. For a very simple API, C2 is often enough; C3 is a selective zoom, not a mandatory step for every container.