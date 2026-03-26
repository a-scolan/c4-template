# Eval-0 — Implement Async Messaging Pattern (Baseline, Run 3)

## Prompt

> Implement an asynchronous messaging pattern in the LikeC4 model. Add a message queue element to decouple the API service from background workers. Use appropriate element kinds and relationship types, then add a container view to show the async pattern.

---

## Response

Adding async decoupling via a message broker. The producer (API) publishes to the broker; the consumer (worker) subscribes. This separates their lifecycles and enables horizontal scaling of workers.

### Model additions

```likec4
model {
  system Backend 'Backend System' {
    uploadApi = Container_Api 'Upload API' {
      technology 'FastAPI'
      description 'Receives upload requests and publishes to queue'
    }

    jobQueue = Container 'Job Queue' {
      technology 'RabbitMQ'
      description 'Message broker decoupling uploads from processing'
      style { shape queue }
    }

    fileProcessor = Container 'File Processor' {
      technology 'Go'
      description 'Subscribes to queue and processes files'
    }

    resultDb = Container_Database 'Result DB' {
      technology 'MongoDB'
    }

    uploadApi -> jobQueue 'Publishes job' { technology 'AMQP' }
    jobQueue -> fileProcessor 'Delivers job' { technology 'AMQP' }
    fileProcessor -> resultDb 'Stores result' { technology 'MongoDB' }
  }
}
```

### View

```likec4
views {
  view queue_pattern of Backend {
    title 'Message Queue Pattern'
    include *
    autoLayout TopBottom
  }
}
```

---

## Observations (baseline, no skill)

- Used `Container` for the queue (should be `Container_Queue` from shared spec)
- Used plain `->` instead of `-[async]->` typed relationship
- Missing `#Queue`, `#Messaging`, `#Async` tags
- No deployment-level modeling of the broker infrastructure
