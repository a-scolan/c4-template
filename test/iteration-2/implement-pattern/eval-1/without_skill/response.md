Apply the workspace’s **queue + worker async processing** pattern.

Use a dedicated `Container_Queue` for RabbitMQ, then model both sides with `async` relationships:

```likec4
model {
  jobs = System_Existing 'Job Processing' {
    api = Container_Api 'Jobs API' {
      technology 'Node.js'
    }

    jobQueue = Container_Queue 'Job Queue' {
      technology 'RabbitMQ'
    }

    worker = Container_ProcessingServer 'Worker' {
      technology 'Python'
    }
  }

  jobs.api -[async]-> jobs.jobQueue 'Publish job' {
    technology 'AMQP'
  }

  jobs.worker -[async]-> jobs.jobQueue 'Consume job' {
    technology 'AMQP'
  }
}
```

The key mistake to avoid is adding a fake synchronous return flow such as `worker -> api` to show completion. That would imply request/response behavior, but this pattern is asynchronous and one-way:

- the API publishes work to the queue
- the worker consumes work from the queue
- completion, status updates, or follow-up actions should be modeled separately if they really exist

So: **queue in the middle, `async` on both interactions, and no invented synchronous return arrow back to the API.**