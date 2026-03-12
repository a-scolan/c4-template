Apply the **async queue + worker** pattern.

A workspace-consistent version is:

```likec4
api = Container_Api 'Job API' {
  technology 'Node.js'
}

queue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
}

worker = Container_ProcessingServer 'Job Worker' {
  technology 'Worker runtime'
}

api -[async]-> queue 'Publish job' {
  technology 'AMQP'
}

worker -[async]-> queue 'Consume job' {
  technology 'AMQP'
}
```

The main mistake to avoid is adding a fake synchronous return flow such as `worker -[calls]-> api`.

Why: this pattern is intentionally **one-way**. The API publishes work, and the worker consumes it asynchronously from RabbitMQ. If you need status feedback, model that as a separate explicit interaction, not as an implied return path.
