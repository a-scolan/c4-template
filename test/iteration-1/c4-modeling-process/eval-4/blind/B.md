It should **not** try to detail everything by itself.

Treat this as a sequencing framework:

1. Keep the **C1/C2 core** as the architectural backbone.
2. Add a **deployment view** only for the production infrastructure that needs to be explained.
3. Add a **dynamic / use-case view** for the nominal user scenario.

So the infrastructure and the user flow should be handled as **targeted follow-up work**, not forced into a single all-purpose response.

In practice:
- use focused help for production infrastructure modeling
- use focused help for the nominal interaction flow
- keep both as additions that come **after** the core C1/C2 model

Deployment and dynamic views are useful when needed, but they are still optional extensions around the main structural model.