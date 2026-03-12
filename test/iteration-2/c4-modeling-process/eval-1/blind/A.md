No—you do **not** need a C3 view for every container.

The decision rule is:

- Stay at **C2** if the API container is simple and its purpose, interfaces, and dependencies are already clear.
- Add **C3** only when the container is **complex, critical, sensitive, or ambiguous** from the C2 view alone.

Typical reasons to create C3 are:
- important internal separation of responsibilities,
- non-obvious control flow,
- security-sensitive internals,
- reliability/performance hotspots,
- many components that need explanation.

So the progression remains **C1 → C2 → C3**, not “always draw C3.” If a simple API is already understandable at C2, skipping C3 is the right choice.