Because this is a before-commit structural change, do a full validation:
1. Confirm the active project and shared taxonomy: the new worker uses a declared element kind, and every new edge uses a declared relationship kind.
2. Verify references: every FQN for the worker and its neighbors resolves in both the model and the C2 view; if any deployment `instanceOf` points to the worker, confirm that target is real.
3. Validate relationships: new traffic to or from the worker should use logical kinds such as `calls`, `async`, `reads`, `writes`, or `uses`; keep protocols like HTTP or Kafka in `technology`, not in the edge type; do not move normal application traffic into deployment relationships.
4. Validate rendering: preview only the impacted C2 view and confirm it shows the parent system boundary, the worker container, and the expected neighbors, with no unrelated elements pulled in by an over-broad include.
5. Do a final sanity pass in the Problems panel or compile output: no unknown kinds, no broken FQNs, no missing labels, and no unexpected extra nodes or edges.

A good before-commit checklist is: kinds valid, FQNs resolve, relationships semantically correct, parent context visible, and the dedicated C2 view renders only what you intended.
