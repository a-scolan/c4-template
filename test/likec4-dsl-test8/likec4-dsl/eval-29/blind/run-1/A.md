A
B puts the body on the wrong hop, C duplicates `frontend -> api` outside the chain, and D breaks `customer -> frontend -> api` into separate statements instead of preserving one chained expression before the single `parallel { ... }` fan-out.
