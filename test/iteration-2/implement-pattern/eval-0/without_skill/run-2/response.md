# Eval-0 — Implement Async Messaging Pattern (Baseline, Run 2)

## Prompt

> Implement an asynchronous messaging pattern in the LikeC4 model. Add a message queue element to decouple the API service from background workers. Use appropriate element kinds and relationship types, then add a container view to show the async pattern.

---

## Response

I will introduce a queue in the container model to enable async decoupling. The queue sits between the API and the worker, receiving published jobs asynchronously.

### Model additions

```likec4
model {
  system App 'Application' {
    apiService = Container_Api 'API Service' {
      technology 'Express.js'
      description 'Handles HTTP requests and enqueues processing jobs'
    }

    messageQueue = Container 'Message Queue' {
      technology 'Apache Kafka'
      description 'Async event stream between producer and consumer'
    }

    workerService = Container 'Worker Service' {
      technology 'Java'
      description 'Processes events from the message queue'
    }

    dataStore = Container_Database 'Data Store' {
      technology 'MySQL'
    }

    apiService -> messageQueue 'Enqueues event' { technology 'AMQP' }
    messageQueue -> workerService 'Dispatches event' { technology 'AMQP' }
    workerService -> dataStore 'Writes result' { technology 'SQL' }
  }
}
```

### View

```likec4
views {
  view messaging_view of App {
    title 'Async Messaging'
    include *
    autoLayout LeftRight
  }
}
```

---

## Observations (baseline, no skill)

- Used `Container` for the queue instead of `Container_Queue` from shared spec
- Relationships use plain `->` instead of the `async` typed relationship kind `-[async]->`
- Did not add `#Queue` or `#Async` tags
- `Container_Api` used correctly for the API service element
