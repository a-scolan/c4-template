No — a detailed C3 view is **not mandatory** for every container.

Use this decision rule:

- Stay at **C2** if the API container is simple and already understandable as a runtime building block.
- Create **C3** only if that container is **internally complex**, **architecturally critical**, **risky**, or hard to explain without showing its main internal components.

In other words, the progression is still **C1 → C2 → C3**, but **C3 is selective**, not automatic. If your API container is straightforward, C2 is enough and you should stop there instead of adding detail that does not improve understanding.