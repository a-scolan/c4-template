You should create the elements first, then write their descriptions.

- For the processing service in the system model, use the `create-element` skill first.
- For the production VM in the deployment model, use the `model-deployment-infrastructure` skill first.

After the elements exist, choose the description format by element type:

- **System element (service/container/component):** use a normal description, and add a `metadata { }` block only if you truly need queryable fields such as `owner` or `regions`.
- **Deployment VM:** use an ops-useful **Markdown table** inside the description. Add deployment metadata only if automation will query values such as IP, OS, CPU, RAM, or RTO.

So the sequence is: create the element with the right creation skill first, then use sparse structured metadata for system-model elements when needed, and a Markdown table for deployment infrastructure.