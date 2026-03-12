Start top-down, not bottom-up.

1. **C1 first**: define the system boundary, the main actors, and the external systems around your SaaS product.
2. **C2 next**: split the system into the runtime containers that make it work, then describe the main interactions between them.
3. **C3 selectively**: only drill into components for containers that are complex, risky, or architecturally central. Do **not** assume every container needs a C3 view.

After the core structure is stable:

4. **Dynamic views are optional**: add them only when you need to explain time-ordered behavior such as a user journey or async workflow. These belong in `views 'Use Cases'`.
5. **Deployment views are optional**: add them only when runtime topology matters, such as environments, zones, VMs, or deployed instances.
6. **Validate at the end**: check that the model is coherent and renderable before you finish.

So the right LikeC4 design order is **C1 → C2 → selective C3**, with **Dynamic** and **Deployment** added later only if they are actually needed.