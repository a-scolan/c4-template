The confusion comes from mixing two different modeling layers and then duplicating the same traffic.

1. Wrong relationship taxonomy in `model {}`
   - `https` is a deployment-side relationship kind for infrastructure links.
   - It should not be used as the logical relationship type in the system model.
   - In the system model, keep the logical relationship kind and put the protocol in the relationship metadata.

   Correct pattern:
   `webapp -[calls]-> api 'Calls API' { technology 'HTTPS' }`

2. Duplicate application traffic in deployment
   - If the deployed applications are created with `instanceOf`, the logical relationships already come from the system model.
   - Copying the same app-to-app traffic again in deployment duplicates meaning and makes the deployment view harder to trust.
   - Deployment relationships should be added only for infrastructure-specific links that are not already represented logically.

Clean fix:
- Change the system-model edge from `-[https]->` to a logical relationship such as `-[calls]->`.
- Keep `technology 'HTTPS'` on that logical relationship.
- Remove the duplicated deployment edge between the deployed apps.
- Keep deployment relationships only for true infrastructure concerns.

So the root cause is not just syntax. It is using a deployment taxonomy in the logical model, then re-modeling inherited traffic a second time in deployment.
