Do not try to force one modeling pass to explain everything.

Treat the core process as a **sequencing framework**:

1. Keep the **C1/C2 static model** as the foundation.
2. Add **production infrastructure** as a **deployment view** when runtime placement, zones, nodes, or environment boundaries matter.
3. Add the **nominal user scenario** as a **dynamic / use-case view** when you need ordered interactions.

These are different concerns:
- **Deployment** explains **where it runs**.
- **Dynamic views** explain **how behavior unfolds over time**.

So they should be handled as **targeted follow-up views**, not as one giant all-purpose diagram. They come **after** the C1/C2 core and remain **optional unless they answer a real question**.