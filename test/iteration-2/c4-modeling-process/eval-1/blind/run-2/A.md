Not always. A detailed C3 view is required only when a container’s internal structure matters for decisions.

Decision rule:
- Create C3 if the container is complex, risky, or actively changing, and stakeholders need internals (components, responsibilities, boundaries) to make design/implementation decisions.
- Skip C3 if the container is simple, stable, and already understandable at C2 level.

Practical triggers for C3:
- Multiple internal modules with non-trivial interactions
- Security/safety/compliance concerns inside the container
- Performance bottlenecks or reliability patterns to explain
- Team handoff where internal ownership must be explicit

If none apply, keep C2 only and revisit C3 later when complexity grows.