A
Only A keeps `customer -> frontend -> api` as one chained expression, attaches the body only to the `frontend -> api` hop, and then preserves a single `parallel { ... }` fan-out from `api`, while B puts the body on the wrong hop, C splits the second hop into a separate statement, and D breaks the chain into two top-level steps.
