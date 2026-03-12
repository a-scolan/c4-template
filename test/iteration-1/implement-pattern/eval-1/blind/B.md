Apply the **async queue + worker** pattern.

Add a dedicated queue for RabbitMQ, for example:

`jobQueue = Container_Queue 'Job Queue' { technology 'RabbitMQ'; description 'Async job processing' }`

Model the flow as two one-way async relationships:

- `vault.api -[async]-> jobQueue 'Publishes jobs'`
- `vault.worker -[async]-> jobQueue 'Consumes jobs'`

The key mistake to avoid is adding a fake synchronous return path such as `vault.worker -[calls]-> vault.api` or any similar “response” relationship. In this pattern, the async flow is **one-way**: the API publishes work, and the worker consumes it from the queue.