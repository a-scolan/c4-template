Short answer: **usually no**—not by default.

An ADR is appropriate only if the GitHub Actions workflow change introduces or changes an **architecture-level decision** (for example: deployment topology, release strategy, security boundaries, artifact architecture, or long-term platform constraints).

Use this quick test:
- If it is routine CI maintenance (lint/test order, caching tweak, version bump), do **not** write an ADR.
- If it changes system-wide technical direction or imposes a lasting constraint, write an ADR.

If you decide to document it, frame it like:
1. Context: what architecture concern the workflow change addresses
2. Decision: the workflow strategy selected
3. Alternatives: other pipeline/deployment approaches considered
4. Consequences: reliability, cost, security, delivery speed trade-offs

So for a typical workflow edit, skip ADR; for a strategic platform/process architecture shift, write one.
