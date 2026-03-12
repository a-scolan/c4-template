Apply the queue + worker pattern.

```likec4
jobQueue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
  description 'Asynchronous job queue'
}

vault.api -[async]-> jobQueue 'Publishes job'
worker -[async]-> jobQueue 'Consumes job'
```

This keeps the async handoff explicit: the API publishes work, and the worker consumes it from the queue. The queue should be a first-class element, not an implied detail hidden in a description.

The main mistake to avoid is adding a synchronous return flow such as `worker -> vault.api`. That would incorrectly suggest request/response behavior. In this pattern, the async flow is one-way through the queue; any later status update should be modeled as a separate explicit interaction if it really exists.