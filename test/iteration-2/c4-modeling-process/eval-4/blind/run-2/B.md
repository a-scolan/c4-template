This skill should not detail everything itself.

Use it to define the modeling sequence and hand off specialized work:
- Keep this skill for process orchestration (what to do first, what depends on what).
- Use deployment-focused capability for production infrastructure modeling.
- Use dynamic/sequence-focused capability for the nominal user scenario.

Suggested order:
1) Lock C2 as the static logical baseline.
2) Create deployment model/views for production runtime.
3) Create dynamic view for the nominal user scenario using the already-defined structure.
4) Run model consistency checks and final polish.

Reason: each artifact (logical, deployment, dynamic) has distinct intent and quality criteria; specialization improves accuracy and maintainability.