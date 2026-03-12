The root cause is that you mixed **two different modeling layers**.

1. In this workspace, `https` is a **deployment-side relationship kind** from `projects/shared/spec-deployment.c4`. It is meant for infrastructure-specific connections.

2. Inside `model {}`, you should use the **logical model relationship taxonomy** from `projects/shared/spec-global.c4`, such as `calls`, and put the transport/protocol in the relationship `technology` field.

So this in the system model is the wrong shape:
- `webapp -[https]-> api`

The clean logical version is:
- `webapp -[calls]-> api 'Calls API' { technology 'HTTPS' }`

3. The second problem is the duplicate deployment traffic. Once the logical relationship exists in the system model, deployed instances should normally inherit it through `instanceOf`. Duplicating the same app-to-app traffic again in deployment makes the model noisy and confusing.

The clean fix is:
- keep the application relationship once in `model {}` using a model kind such as `calls`
- put `technology 'HTTPS'` on that logical relationship
- remove the duplicate deployment relationship between the deployed apps if it is the same traffic
- keep deployment relationships only for **infrastructure-specific** links that are not already represented logically

So the fix is not just syntax swapping. The root cause is:
- **wrong taxonomy in the system model** (`https` used where a model relationship kind should be used), and
- **duplicated deployment traffic** that should instead be inherited via `instanceOf`.