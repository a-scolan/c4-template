The confusion comes from mixing two different layers of modeling.

1. Wrong taxonomy in `model {}`
   - `https` is a deployment-side relationship kind, not a logical system-model relationship kind.
   - In the system model, use a logical relationship such as `calls`, then put the protocol in the relationship `technology`.

2. Duplicate traffic in deployment
   - You then copied the same application traffic again between deployed apps just to show protocol details.
   - That duplicates information the deployment instances should already inherit from their `instanceOf` model elements.

Clean fix:
- Correct the logical edge in `model {}` to `webapp -[calls]-> api 'Makes API requests' { technology 'HTTPS' }`.
- Remove the duplicate deployment relationship between the deployed apps.
- Keep deployment relationships only for infrastructure-specific links that do not exist at the logical model level.

Why this is the root-cause fix:
- The real problem is not just syntax; it is taxonomy leakage between the system model and deployment model.
- Once the protocol lives on the logical relationship and deployment instances inherit that edge, the diagram becomes consistent again.
