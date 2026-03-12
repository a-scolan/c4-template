No — a C3 view is **not mandatory** for every container.

Use this decision rule:

- Stay at **C2** if the container is simple and already understandable as a runtime building block.
- Create **C3** only when the container is **complex**, **architecturally central**, **risky**, or needs deeper internal detail for the model to be clear.

So for a very simple API container, if its role and interactions are already clear in **C1 → C2**, you can stop at **C2**. C3 is selective, not automatic.