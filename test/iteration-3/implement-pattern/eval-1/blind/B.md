Apply the Async queue + worker pattern.

Minimal scaffold:
jobQueue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
}

worker = Container_ProcessingServer 'Job Worker' {
  technology 'Worker runtime'
}

api -[async]-> jobQueue 'Publishes job' {
  technology 'AMQP'
}

worker -[async]-> jobQueue 'Consumes job' {
  technology 'AMQP'
}

Mistake to avoid:
- Do not add a fake synchronous return such as `worker -> api` or `worker -[calls]-> api 'Returns result'`.
- In this pattern the async flow is one-way through the queue; if you later need a callback or status update, model that as a second explicit interaction, not as the return leg of the queue flow.

Substitute:
- `api`: your existing API container
- `worker`: the concrete worker name and, if needed, a different valid container kind
- queue name and technologies to match your runtime
