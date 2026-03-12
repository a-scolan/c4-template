The root cause is that two different modeling layers got mixed together.

1. `webapp -[https]-> api` is wrong inside `model {}`.
   `https` is a deployment-side relationship kind, not a logical system-model relationship kind. In the system model, keep a functional relationship such as `calls`, and put the protocol in the relationship technology.

   The clean logical fix is:
   `webapp -[calls]-> api 'Makes API requests' { technology 'HTTPS' }`

2. The duplicate deployment traffic is also a modeling mistake.
   If deployed applications `instanceOf` the logical containers, the application relationship should be inherited from the system model. Repeating the same app-to-app traffic again in deployment just to show the protocol creates duplication and confusion.

3. Clean fix.
   - change the system-model edge from `-[https]->` to a valid model relationship such as `-[calls]->`
   - keep `technology 'HTTPS'` on that logical relationship
   - remove the duplicate deployment relationship between the deployed apps
   - keep deployment-only relationships only when they represent infrastructure-specific communication that is not already modeled logically

So the real issue is not just syntax. It is a taxonomy mix-up in the system model plus duplicated relationships across logical and deployment layers.