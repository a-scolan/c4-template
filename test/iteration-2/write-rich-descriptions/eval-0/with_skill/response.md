The description comes **after** the element exists.

- For the **processing service** (a system-model element), use `create-element` first.
- For the **production VM** (deployment infrastructure), use `model-deployment-infrastructure` first.

Once each element is created, choose the description format by element type:

- **System model element**: use a prose `description`, and add a sparse `metadata {}` block **only** if you will query or filter fields such as `owner` or `regions`.
- **Deployment VM**: use a **Markdown table** inside the description for ops-facing facts. Put network interfaces first. Add `metadata {}` only if automation needs to query the same values.

Short version:
1. Create the service with `create-element`.
2. Create the VM with `model-deployment-infrastructure`.
3. Then use **optional `metadata {}` for the system element** and a **Markdown table for the VM**.
