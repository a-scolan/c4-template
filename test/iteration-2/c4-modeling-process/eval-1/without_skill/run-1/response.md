Usually **no**—you do not always need a detailed C3 view for a simple API container.

Decision rule:

- Create a C3 view **only if** it improves an important decision:
  - multiple internal components with distinct responsibilities,
  - non-trivial security/data/control flow,
  - ownership boundaries across teams,
  - frequent change hotspots needing explicit contracts.
- Skip (or defer) C3 when the container is small, cohesive, and well-understood from C2.

Practical test: if stakeholders can make design and delivery decisions confidently from C2 + container docs, C3 is optional.